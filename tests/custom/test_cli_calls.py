"""Unit tests for `smallestai calls …` — rendering + SDK wiring with a fake client."""

import types

import pytest
from typer.testing import CliRunner

from smallestai.cli.calls import _fmt_dur, initialise_calls_app

runner = CliRunner()


class _Resp:
    def __init__(self, data):
        self.data = data


def _obj(**kw):
    return types.SimpleNamespace(**kw)


class FakeCalls:
    def __init__(self, logs=None, call=None):
        self._logs = logs or []
        self._call = call
        self.list_kwargs = None

    def list(self, **kw):
        self.list_kwargs = kw
        return _Resp(_obj(logs=self._logs))

    def get(self, id):
        return _Resp(self._call)


class FakeClient:
    def __init__(self, calls):
        self.atoms = _obj(calls=calls)


@pytest.fixture
def app_with(monkeypatch):
    def _make(calls):
        monkeypatch.setattr("smallestai.cli.calls.make_client", lambda auth: FakeClient(calls))
        return initialise_calls_app(auth_client=None)

    return _make


def test_fmt_dur():
    assert _fmt_dur(43.4) == "43.4s"
    assert _fmt_dur(89) == "1m29s"
    assert _fmt_dur(None) == "—"


def test_list_renders_and_passes_filters(app_with):
    calls = FakeCalls(
        logs=[
            _obj(
                call_id="CALL-1",
                type="telephony_outbound",
                status="completed",
                duration=89,
                from_="+111",
                to="+222",
                created_at="2026-08-04T09:06:07.000Z",
                recording_url="u",
            ),
        ]
    )
    app = app_with(calls)
    res = runner.invoke(app, ["list", "--agent-id", "AG1", "--type", "telephony_outbound", "--limit", "5"])
    assert res.exit_code == 0, res.output
    assert "CALL-1" in res.output
    assert "outbound" in res.output  # telephony_ stripped
    # filters forwarded to the SDK
    assert calls.list_kwargs == {"limit": 5, "agent_ids": "AG1", "call_types": "telephony_outbound"}


def test_get_shows_fields_and_recording(app_with):
    call = _obj(
        status="completed",
        type="telephony_outbound",
        duration=89,
        from_="+1",
        to="+2",
        transcript=[_obj(role="user", content="hi")],
        call_cost=0.17,
        call_failure_reason=None,
        recording_url="https://rec/x.wav",
    )
    app = app_with(FakeCalls(call=call))
    res = runner.invoke(app, ["get", "CALL-9"])
    assert res.exit_code == 0, res.output
    assert "completed" in res.output
    assert "turns" in res.output and "1" in res.output
    assert "https://rec/x.wav" in res.output


def test_transcript_prints_turns(app_with):
    call = _obj(transcript=[_obj(role="user", content="hello"), _obj(role="assistant", content="hi there")])
    app = app_with(FakeCalls(call=call))
    res = runner.invoke(app, ["transcript", "CALL-9"])
    assert res.exit_code == 0, res.output
    assert "hello" in res.output and "hi there" in res.output


def test_transcript_empty(app_with):
    call = _obj(transcript=[])
    app = app_with(FakeCalls(call=call))
    res = runner.invoke(app, ["transcript", "CALL-9"])
    assert res.exit_code == 0
    assert "No transcript" in res.output


def test_recording_absent(app_with):
    call = _obj(recording_url=None, recording_dual_url=None)
    app = app_with(FakeCalls(call=call))
    res = runner.invoke(app, ["recording", "CALL-9"])
    assert res.exit_code == 0
    assert "No recording" in res.output
