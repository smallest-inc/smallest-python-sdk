"""SSE parsing for build logs / call events, and the call-event renderers."""

import asyncio

import pytest

import smallestai.cli.calls as calls
from smallestai.cli.lib.atoms import AtomsAPIClient


class _FakeStream:
    def __init__(self, lines):
        self._lines = lines

    def raise_for_status(self):
        return None

    async def aiter_lines(self):
        for ln in self._lines:
            yield ln

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class _FakeClient:
    def __init__(self, lines):
        self._lines = lines

    def stream(self, method, url, headers=None):
        return _FakeStream(self._lines)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


def test_stream_sse_parses_data_frames(monkeypatch):
    lines = [
        'data: {"event_type": "sse_init"}',
        "",
        ": keep-alive",
        'data: {"event_type": "user_transcription", "user_transcription_text": "hi"}',
        "data: not-json",
        'data:{"event_type":"call_end"}',
    ]
    monkeypatch.setattr(calls.httpx, "AsyncClient", lambda *a, **k: _FakeClient(lines))
    client = AtomsAPIClient()

    async def _collect():
        return [ev async for ev in client._stream_sse("http://x", "tok")]

    got = asyncio.run(_collect())
    assert [e["event_type"] for e in got] == ["sse_init", "user_transcription", "call_end"]
    assert got[1]["user_transcription_text"] == "hi"


def test_render_event_shapes(capsys):
    calls._render_event({"event_type": "user_transcription", "user_transcription_text": "hello"})
    calls._render_event({"event_type": "tts_completed", "tts_text": "hi there"})
    calls._render_event({"event_type": "turn_latency", "turn_latency": 820})
    calls._render_event({"event_type": "agent_error", "error": "boom"})
    calls._render_event({"event_type": "some_new_type", "foo": 1})
    out = capsys.readouterr().out
    assert "user" in out and "hello" in out
    assert "agent" in out and "hi there" in out
    assert "820" in out
    assert "boom" in out
    assert "some_new_type" in out  # unknown types still surface


def test_render_transcript_event_only_turns(capsys):
    calls._render_transcript_event({"event_type": "turn_latency", "turn_latency": 1})
    calls._render_transcript_event({"event_type": "user_transcription", "user_transcription_text": "q"})
    calls._render_transcript_event({"event_type": "tts_completed", "tts_text": "a"})
    out = capsys.readouterr().out
    assert "q" in out and "a" in out
    assert "latency" not in out  # non-turn events are dropped


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
