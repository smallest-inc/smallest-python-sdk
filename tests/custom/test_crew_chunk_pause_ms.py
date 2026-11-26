"""SDKAgentLLMResponseChunkEvent.pause_ms is an optional post-chunk pause (PRO-3555).

A crew can set ``pause_ms`` on a response chunk so the orchestrator inserts that much
silence after the chunk's speech. It is a lightweight alternative to SSML ``<break>``,
which Smallest Waves/Lightning TTS does not support. The field defaults to None and must
survive a wire round-trip so older and newer orchestrators interoperate.
"""

import json

from smallestai.atoms.crew.events import SDKAgentLLMResponseChunkEvent
from smallestai.atoms.crew.session import EventCodec


def test_pause_ms_defaults_to_none():
    ev = SDKAgentLLMResponseChunkEvent(text="Let me check...")
    assert ev.pause_ms is None
    assert ev.text == "Let me check..."


def test_pause_ms_is_settable():
    ev = SDKAgentLLMResponseChunkEvent(text="Let me check...", pause_ms=600)
    assert ev.pause_ms == 600


def test_pause_ms_survives_a_wire_round_trip():
    codec = EventCodec()
    sent = SDKAgentLLMResponseChunkEvent(text="One sec", pause_ms=500)

    wire = json.loads(codec.encode(sent))
    assert wire["type"] == "agent.llm.response.chunk"
    assert wire["pause_ms"] == 500

    received = codec.decode(wire)
    assert isinstance(received, SDKAgentLLMResponseChunkEvent)
    assert received.pause_ms == 500
    assert received.text == "One sec"


def test_a_chunk_without_pause_ms_still_decodes():
    # An older crew (or a chunk with no pause) sends no pause_ms; it reads back as None.
    received = EventCodec().decode({"type": "agent.llm.response.chunk", "text": "hi"})
    assert isinstance(received, SDKAgentLLMResponseChunkEvent)
    assert received.pause_ms is None
    assert received.text == "hi"
