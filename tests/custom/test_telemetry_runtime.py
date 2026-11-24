"""sdk_method_called runtime telemetry: allowlisted payload, opt-outs, never blocks or raises,
success and failure reported, and the API call itself is left untouched."""

import asyncio
import json
import os
import queue
import threading
import time
import typing

import httpx
import pytest

import smallestai.telemetry as telemetry
from smallestai import AsyncSmallestAI, SmallestAI
from smallestai.core import _telemetry_http_client as hook
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
    transport = telemetry.method_properties(
        "waves.voices.get_all_voice_models", success=False, error_type="ReadTimeout"
    )
    assert set(transport) == set(telemetry.ALLOWED_METHOD_PROPERTIES - {"http_status"})
    assert transport["success"] is False and transport["error_type"] == "ReadTimeout"
    http = telemetry.method_properties(
        "waves.voices.get_all_voice_models", success=False, error_type="ApiError", http_status=401
    )
    assert set(http) == set(telemetry.ALLOWED_METHOD_PROPERTIES)
    assert http["http_status"] == 401


def test_http_status_only_on_failures_and_only_as_a_valid_int():
    assert "http_status" not in telemetry.method_properties("m", success=True, http_status=500)
    for bad in ("401", 401.0, True, 0, 99, 600, -1, None):
        props = telemetry.method_properties("m", success=False, error_type="ApiError", http_status=bad)  # type: ignore[arg-type]
        assert "http_status" not in props, bad


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
    telemetry._send_batch(
        [
            telemetry.method_properties("waves.voices.get_all_voice_models", success=True),
            telemetry.method_properties(
                "atoms.user.get_user_details", success=False, error_type="ApiError", http_status=403
            ),
        ]
    )

    assert sent["url"] == "https://us.i.posthog.com/batch/"
    assert sent["timeout"] <= 2.0
    assert set(sent["headers"]) == {"Content-type"}
    body = sent["body"]
    assert set(body) == {"api_key", "batch"}
    assert body["api_key"].startswith("phc_")  # PostHog's public write-only project key
    event, failed_event = body["batch"]
    assert set(event) == set(failed_event) == {"event", "distinct_id", "properties"}
    assert event["event"] == "sdk_method_called"
    assert len(event["distinct_id"]) == 32 and event["distinct_id"] == telemetry.install_id()
    directives = {"$geoip_disable", "$process_person_profile"}
    assert (
        set(event["properties"])
        == set(telemetry.ALLOWED_METHOD_PROPERTIES - {"error_type", "http_status"}) | directives
    )
    assert set(failed_event["properties"]) == set(telemetry.ALLOWED_METHOD_PROPERTIES) | directives
    assert failed_event["properties"]["http_status"] == 403
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
    assert "http_status" not in event


def test_http_failure_is_reported_and_the_sdk_error_is_unchanged(events):
    def unauthorized(request):
        return httpx.Response(401, json={"message": "bad key"})

    with pytest.raises(ApiError) as with_telemetry:
        _client(unauthorized).waves.voices.get_all_voice_models()
    (event,) = _drain(events)
    assert event == {**event, "success": False, "error_type": "ApiError", "method": "waves.voices.get_all_voice_models"}
    assert event["http_status"] == 401 and type(event["http_status"]) is int
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
    assert "http_status" not in event  # transport errors never carry a status
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
    assert failed["http_status"] == 500
    assert "http_status" not in ok


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
    # pytest sets PYTEST_CURRENT_TEST while this test runs, so the real detector says "off".
    assert os.environ.get("PYTEST_CURRENT_TEST")
    assert telemetry._in_test_or_ci() is True
    assert telemetry.runtime_enabled() is False
    # Merely having pytest imported (e.g. a library that imports it) is not enough.
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    assert telemetry._in_test_or_ci() is False
    monkeypatch.setenv("CI", "true")
    assert telemetry._in_test_or_ci() is True


def _exercise_all_hook_paths(handler) -> None:
    client = _client(handler)
    client.waves.voices.get_all_voice_models()
    for _ in client.atoms.live_transcripts.subscribe_to_live_events(call_id="call-1"):
        pass

    async def run():
        async_client = _async_client(handler)
        await async_client.waves.voices.get_all_voice_models()
        async for _ in async_client.atoms.live_transcripts.subscribe_to_live_events(call_id="call-1"):
            pass

    asyncio.run(run())


def _ok_or_sse(request: httpx.Request) -> httpx.Response:
    if request.url.path.endswith("events"):
        return httpx.Response(200, content=b"data: {}\n\n", headers={"content-type": "text/event-stream"})
    return _ok(request)


@pytest.mark.parametrize("opt_out", ["env", "pytest"])
def test_opt_out_skips_frame_walking(events, monkeypatch, opt_out):
    walks = {"n": 0}
    real_walk = hook._caller_method_name

    def counting_walk():
        walks["n"] += 1
        return real_walk()

    monkeypatch.setattr(hook, "_caller_method_name", counting_walk)
    if opt_out == "env":
        monkeypatch.setenv("SMALLEST_TELEMETRY_DISABLED", "1")
    else:  # undo the fixture's override: the real pytest detector turns telemetry off
        monkeypatch.setattr(telemetry, "_in_test_or_ci", lambda: True)
    _exercise_all_hook_paths(_ok_or_sse)
    assert walks["n"] == 0
    assert _drain(events) == []

    # Sanity: with telemetry on, the same calls do walk (sync + async, request + stream).
    monkeypatch.delenv("SMALLEST_TELEMETRY_DISABLED", raising=False)
    monkeypatch.setattr(telemetry, "_in_test_or_ci", lambda: False)
    _exercise_all_hook_paths(_ok_or_sse)
    assert walks["n"] == 4
    assert len(_drain(events)) == 4


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


# --- fork safety --------------------------------------------------------------------------


def test_after_fork_hook_resets_queue_and_lock(monkeypatch):
    monkeypatch.setattr(telemetry, "_queue", queue.Queue())
    monkeypatch.setattr(telemetry, "_queue_pid", 12345)
    held = threading.Lock()
    held.acquire()
    monkeypatch.setattr(telemetry, "_queue_lock", held)
    telemetry._reset_after_fork()
    assert telemetry._queue is None
    assert telemetry._queue_pid is None
    assert telemetry._queue_lock is not held and not telemetry._queue_lock.locked()


def test_fork_hook_is_registered_once(monkeypatch):
    if not hasattr(os, "register_at_fork"):
        pytest.skip("os.register_at_fork is POSIX-only")
    registered = []
    monkeypatch.setattr(telemetry, "_fork_hook_registered", False)
    monkeypatch.setattr(telemetry.os, "register_at_fork", lambda **kw: registered.append(kw))
    monkeypatch.setattr(telemetry, "_queue", None)
    monkeypatch.setattr(telemetry, "_worker", lambda q: None)
    telemetry._get_queue()
    monkeypatch.setattr(telemetry, "_queue", None)
    telemetry._get_queue()
    assert registered == [{"after_in_child": telemetry._reset_after_fork}]


@pytest.mark.skipif(not hasattr(os, "fork"), reason="needs os.fork")
def test_forked_child_does_not_deadlock_on_a_lock_held_at_fork_time(monkeypatch):
    monkeypatch.setattr(telemetry, "_worker", lambda q: None)  # no network, no real worker
    monkeypatch.setattr(telemetry, "_queue", None)
    monkeypatch.setattr(telemetry, "_queue_pid", None)
    monkeypatch.setattr(telemetry, "_queue_lock", threading.Lock())
    parent_q = telemetry._get_queue()  # registers the at-fork hook
    lock = telemetry._queue_lock
    lock.acquire()  # simulate another parent thread holding the lock at fork time
    try:
        pid = os.fork()
        if pid == 0:  # child: must get fresh state and a new queue without blocking
            code = 1
            try:
                ok_state = telemetry._queue is None and not telemetry._queue_lock.locked()
                child_q = telemetry._get_queue()
                code = 0 if ok_state and child_q is not parent_q else 2
            finally:
                os._exit(code)
        deadline = time.monotonic() + 5
        while True:
            done, status = os.waitpid(pid, os.WNOHANG)
            if done:
                break
            if time.monotonic() > deadline:
                os.kill(pid, 9)
                os.waitpid(pid, 0)
                pytest.fail("forked child deadlocked in _get_queue()")
            time.sleep(0.01)
        assert os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0
    finally:
        lock.release()
