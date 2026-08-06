"""Anonymous opt-out telemetry: opt-out, anonymous id, no-PII payload, non-blocking."""
import smallestai.telemetry as telemetry


def test_opt_out_env_vars(monkeypatch):
    monkeypatch.delenv("DO_NOT_TRACK", raising=False)
    monkeypatch.setenv("SMALLESTAI_TELEMETRY", "0")
    assert telemetry.is_enabled() is False
    monkeypatch.setenv("SMALLESTAI_TELEMETRY", "1")
    assert telemetry.is_enabled() is True
    monkeypatch.setenv("DO_NOT_TRACK", "1")
    assert telemetry.is_enabled() is False


def test_install_id_is_anonymous_and_persists(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    first = telemetry.install_id()
    second = telemetry.install_id()
    assert first == second
    assert len(first) == 32  # a uuid4 hex, not an account id


def test_disabled_capture_sends_nothing(monkeypatch):
    monkeypatch.setenv("SMALLESTAI_TELEMETRY", "0")
    calls = []
    monkeypatch.setattr(telemetry, "_post", lambda e, p: calls.append(e))
    telemetry.capture("cli_invoked", {"command": "agent-crew"})
    assert calls == []


def test_enabled_capture_payload_has_versions_and_no_secrets(monkeypatch, tmp_path):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.delenv("SMALLESTAI_TELEMETRY", raising=False)
    monkeypatch.delenv("DO_NOT_TRACK", raising=False)

    captured = {}

    def fake_post(event, props):
        captured["event"] = event
        captured["props"] = props

    class _ImmediateThread:
        def __init__(self, target, args=(), daemon=None):
            self._target, self._args = target, args

        def start(self):
            self._target(*self._args)

    monkeypatch.setattr(telemetry, "_post", fake_post)
    monkeypatch.setattr(telemetry.threading, "Thread", _ImmediateThread)

    telemetry.capture("cli_invoked", {"command": "agent-crew"})

    assert captured["event"] == "cli_invoked"
    props = captured["props"]
    assert {"sdk_version", "python_version", "os"} <= set(props)
    assert props["command"] == "agent-crew"
    # never leak identifying/secret keys
    blob = str(props).lower()
    for banned in ("api_key", "sk_", "token", "phone", "prompt", "transcript"):
        assert banned not in blob


def test_first_run_notice_shows_once(monkeypatch, tmp_path, capsys):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.delenv("SMALLESTAI_TELEMETRY", raising=False)
    monkeypatch.delenv("DO_NOT_TRACK", raising=False)
    telemetry.maybe_show_first_run_notice()
    telemetry.maybe_show_first_run_notice()
    out = capsys.readouterr().out
    assert out.count("anonymous usage telemetry") == 1


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
