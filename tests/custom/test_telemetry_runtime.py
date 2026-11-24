"""sdk_method_called runtime telemetry: allowlisted payload, opt-outs, never blocks or raises,
success and failure reported, and the API call itself is left untouched."""

import asyncio
import json
import queue
import threading
import time
import typing

import httpx
import pytest

import smallestai.telemetry as telemetry
from smallestai import AsyncSmallestAI, SmallestAI
from smallestai.core.api_error import ApiError
from smallestai.core.http_client import AsyncHttpClient, HttpClient

_OPT_OUT_VARS = ("SMALLEST_TELEMETRY_DISABLED", "DO_NOT_TRACK", "SMALLESTAI_TELEMETRY", "CI")
_FAKE_KEY = "sk_test_do_not_send_me"
_VOICES_OK: typing.Dict[str, typing.Any] = {"voices": []}


@pytest.fixture
def events(monkeypatch, tmp_path) -> "queue.Queue[typing.Dict[str, typing.Any]]":
    """Telemetry on (as for a real user), with events captured in a local queue, no network."""
    for var in _OPT_OUT_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(telemetry, "_in_test_or_ci", lambda: False)
    q: "queue.Queue[typing.Dict[str, typing.Any]]" = queue.Queue()
    monkeypatch.setattr(telemetry, "_get_queue", lambda: q)
    return q


def _drain(q: "queue.Queue[typing.Dict[str, typing.Any]]") -> typing.List[typing.Dict[str, typing.Any]]:
    out = []
    while not q.empty():
        out.append(q.get_nowait())
    return out


def _client(handler, **kwargs) -> SmallestAI:
    return SmallestAI(api_key=_FAKE_KEY, httpx_client=httpx.Client(transport=httpx.MockTransport(handler)), **kwargs)


def _async_client(handler, **kwargs) -> AsyncSmallestAI:
    return AsyncSmallestAI(
        api_key=_FAKE_KEY, httpx_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)), **kwargs
    )


def _ok(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json=_VOICES_OK)


# --- payload -----------------------------------------------------------------------


def test_method_properties_are_exactly_the_allowlist():
    ok = telemetry.method_properties("waves.voices.get_all_voice_models", success=True)
    assert set(ok) == {"sdk_version", "python_version", "os", "method", "success"}
    failed = telemetry.method_properties("waves.voices.get_all_voice_models", success=False, error_type="ApiError")
    assert set(failed) == set(telemetry.ALLOWED_METHOD_PROPERTIES)
    assert failed["success"] is False and failed["error_type"] == "ApiError"


def test_method_and_error_names_that_look_like_data_are_replaced():
    props = telemetry.method_properties("https://x.io/a?key=sk_1 2", success=False, error_type="boom: secret text")
    assert props["method"] == "unknown"
    assert props["error_type"] == "Error"


def test_wire_payload_has_only_allowlist_plus_posthog_directives(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.delenv("SMALLEST_TELEMETRY_KEY", raising=False)
    monkeypatch.delenv("SMALLEST_TELEMETRY_HOST", raising=False)
    sent: typing.Dict[str, typing.Any] = {}

    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(request, timeout):
        sent["url"] = request.full_url
        sent["headers"] = dict(request.header_items())
        sent["body"] = json.loads(request.data)
        sent["timeout"] = timeout
        return _Resp()

    monkeypatch.setattr(telemetry.urllib.request, "urlopen", fake_urlopen)
    telemetry._send_batch([telemetry.method_properties("waves.voices.get_all_voice_models", success=True)])

    assert sent["url"] == "https://us.i.posthog.com/batch/"
    assert sent["timeout"] <= 2.0
    assert set(sent["headers"]) == {"Content-type"}
    body = sent["body"]
    assert set(body) == {"api_key", "batch"}
    assert body["api_key"].startswith("phc_")  # PostHog's public write-only project key
    (event,) = body["batch"]
    assert set(event) == {"event", "distinct_id", "properties"}
    assert event["event"] == "sdk_method_called"
    assert len(event["distinct_id"]) == 32 and event["distinct_id"] == telemetry.install_id()
    assert set(event["properties"]) == set(telemetry.ALLOWED_METHOD_PROPERTIES - {"error_type"}) | {
        "$geoip_disable",
        "$process_person_profile",
    }
    assert event["properties"]["$geoip_disable"] is True
    assert event["properties"]["$process_person_profile"] is False


def test_key_and_host_can_be_overridden_by_env(monkeypatch):
    monkeypatch.setenv("SMALLEST_TELEMETRY_KEY", "phc_override")
    monkeypatch.setenv("SMALLEST_TELEMETRY_HOST", "https://eu.i.posthog.com/")
    assert telemetry._project_key() == "phc_override"
    assert telemetry._host() == "https://eu.i.posthog.com"


def test_real_call_event_never_contains_key_url_or_payload(events):
    client = _client(_ok)
    client.waves.voices.get_all_voice_models()
    (event,) = _drain(events)
    assert set(event) <= telemetry.ALLOWED_METHOD_PROPERTIES
    blob = json.dumps(event)
    for banned in (_FAKE_KEY, "Bearer", "http", "voice/get-all-models", 'voices": []'):
        assert banned not in blob


# --- success and failure -------------------------------------------------------------


def test_success_is_reported_with_the_sdk_method_name(events):
    _client(_ok).waves.voices.get_all_voice_models()
    (event,) = _drain(events)
    assert event["method"] == "waves.voices.get_all_voice_models"
    assert event["success"] is True
    assert "error_type" not in event


def test_http_failure_is_reported_and_the_sdk_error_is_unchanged(events):
    def unauthorized(request):
        return httpx.Response(401, json={"message": "bad key"})

    with pytest.raises(ApiError) as with_telemetry:
        _client(unauthorized).waves.voices.get_all_voice_models()
    (event,) = _drain(events)
    assert event == {**event, "success": False, "error_type": "ApiError", "method": "waves.voices.get_all_voice_models"}
    assert "bad key" not in json.dumps(event)

    with pytest.raises(ApiError) as without_telemetry:
        _client(unauthorized, telemetry=False).waves.voices.get_all_voice_models()
    assert type(with_telemetry.value) is type(without_telemetry.value)
    assert with_telemetry.value.status_code == without_telemetry.value.status_code == 401
    assert with_telemetry.value.body == without_telemetry.value.body


def test_transport_failure_is_reported_by_class_name_and_reraised(events):
    def down(request):
        raise httpx.ConnectError("connection refused to secret-host")

    with pytest.raises(httpx.ConnectError, match="secret-host"):
        _client(down, max_retries=0).waves.voices.get_all_voice_models()
    (event,) = _drain(events)
    assert event["success"] is False
    assert event["error_type"] == "ConnectError"
    assert "secret-host" not in json.dumps(event)


def test_retries_are_counted_once(events):
    calls = {"n": 0}

    def flaky(request):
        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(429, headers={"Retry-After": "0"}, json={})
        return httpx.Response(200, json=_VOICES_OK)

    _client(flaky).waves.voices.get_all_voice_models()
    assert calls["n"] == 2
    (event,) = _drain(events)
    assert event["success"] is True


def test_async_success_and_failure(events):
    async def run():
        await _async_client(_ok).waves.voices.get_all_voice_models()
        with pytest.raises(ApiError):
            await _async_client(lambda r: httpx.Response(500, json={})).waves.voices.get_all_voice_models(
                request_options={"max_retries": 0}
            )

    asyncio.run(run())
    ok, failed = _drain(events)
    assert ok["method"] == failed["method"] == "waves.voices.get_all_voice_models"
    assert ok["success"] is True
    assert failed["success"] is False and failed["error_type"] == "ApiError"


def test_streaming_endpoint_is_recorded_once(events):
    def sse(request):
        return httpx.Response(200, content=b"data: {}\n\n", headers={"content-type": "text/event-stream"})

    client = _client(sse)
    for _ in client.atoms.live_transcripts.subscribe_to_live_events(call_id="call-1"):
        pass
    (event,) = _drain(events)
    assert event["method"] == "atoms.live_transcripts.subscribe_to_live_events"
    assert event["success"] is True


# --- opt-outs -------------------------------------------------------------------------


@pytest.mark.parametrize(
    "var,value",
    [("SMALLEST_TELEMETRY_DISABLED", "1"), ("SMALLEST_TELEMETRY_DISABLED", "true"), ("DO_NOT_TRACK", "1")],
)
def test_env_opt_out_sends_nothing(events, monkeypatch, var, value):
    monkeypatch.setenv(var, value)
    assert telemetry.is_enabled() is False
    _client(_ok).waves.voices.get_all_voice_models()
    assert _drain(events) == []


def test_client_flag_opt_out_uses_the_plain_generated_client(events):
    client = _client(_ok, telemetry=False)
    assert type(client._client_wrapper.httpx_client) is HttpClient
    client.waves.voices.get_all_voice_models()
    async_client = _async_client(_ok, telemetry=False)
    assert type(async_client._client_wrapper.httpx_client) is AsyncHttpClient
    asyncio.run(async_client.waves.voices.get_all_voice_models())
    assert _drain(events) == []


def test_off_under_pytest_and_ci(monkeypatch):
    for var in _OPT_OUT_VARS:
        monkeypatch.delenv(var, raising=False)
    # This test itself runs under pytest, so the real detector must say "off".
    assert telemetry._in_test_or_ci() is True
    assert telemetry.runtime_enabled() is False
    monkeypatch.setattr(telemetry.sys, "modules", {})
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    assert telemetry._in_test_or_ci() is False
    monkeypatch.setenv("CI", "true")
    assert telemetry._in_test_or_ci() is True


def test_constructor_accepts_telemetry_flag():
    # Regen guard: client.py is generated. If a regen drops the `telemetry` kwarg this fails.
    assert SmallestAI(api_key="k", telemetry=False)._client_wrapper.httpx_client.__class__ is HttpClient
    assert AsyncSmallestAI(api_key="k", telemetry=False)._client_wrapper.httpx_client.__class__ is AsyncHttpClient


# --- never blocks, never raises ---------------------------------------------------------


def test_network_failure_never_raises():
    def boom(*a, **k):
        raise OSError("network down")

    original = telemetry.urllib.request.urlopen
    telemetry.urllib.request.urlopen = boom
    try:
        telemetry._send_batch([telemetry.method_properties("m", success=True)])  # must not raise
    finally:
        telemetry.urllib.request.urlopen = original


def test_slow_or_failing_network_never_blocks_the_caller(monkeypatch, tmp_path):
    for var in _OPT_OUT_VARS:
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setattr(telemetry, "_in_test_or_ci", lambda: False)
    monkeypatch.setattr(telemetry, "_queue", None)
    monkeypatch.setattr(telemetry, "_queue_pid", None)
    sending = threading.Event()
    release = threading.Event()
    calls = {"n": 0}

    def hanging_then_failing(request, timeout):
        calls["n"] += 1
        sending.set()
        if calls["n"] == 1:
            release.wait(5)
        raise OSError("network down")

    monkeypatch.setattr(telemetry.urllib.request, "urlopen", hanging_then_failing)

    start = time.monotonic()
    _client(_ok).waves.voices.get_all_voice_models()
    assert sending.wait(2), "worker never picked up the event"
    # Worker is now stuck in a hanging send; more calls must still return immediately.
    for _ in range(telemetry._QUEUE_MAX + 50):  # overfill the queue: extra events are dropped
        telemetry.record_method("m", success=True)
    _client(_ok).waves.voices.get_all_voice_models()
    assert time.monotonic() - start < 1.5
    release.set()
    # Worker survives the exception and keeps draining.
    deadline = time.monotonic() + 3
    while calls["n"] < 2 and time.monotonic() < deadline:
        time.sleep(0.01)
    assert calls["n"] >= 2


def test_telemetry_bugs_never_break_the_api_call(events, monkeypatch):
    def broken(*a, **k):
        raise RuntimeError("telemetry bug")

    monkeypatch.setattr(telemetry, "method_properties", broken)
    response = _client(_ok).waves.voices.with_raw_response.get_all_voice_models()
    assert response.data.voices == []
    monkeypatch.setattr(telemetry, "_get_queue", broken)
    telemetry.record_method("m", success=True)  # must not raise
