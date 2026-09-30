"""Crew premise validation — the code-first agent core must work end to end.

Node-level, in-process, deterministic (fake LLM, no network). This is the tight
feedback loop for the premise in crew/CONTEXT.md: an LLM request drives
generate_response, chunks stream out, speak voices only when running, a failing
turn surfaces an error but still closes the response, a background node observes
silently, an interrupt does not break the node, and events round-trip the wire.
"""

import json
import unittest
from unittest import mock

from smallestai.atoms.crew.events import (
    SDKAgentErrorEvent,
    SDKAgentLLMResponseChunkEvent,
    SDKAgentLLMResponseEndEvent,
    SDKAgentLLMResponseStartEvent,
    SDKAgentSpeakEvent,
    SDKSystemControlInterruptEvent,
    SDKSystemLLMRequestEvent,
)
from smallestai.atoms.crew.nodes import BackgroundCrewNode, OutputCrewNode
from smallestai.atoms.crew.session import EventCodec


class _FakeLLMNode(OutputCrewNode):
    """Deterministic output node: generate_response yields fixed chunks (or raises)."""

    def __init__(self, chunks=("Hello", " world"), raise_exc=None, is_interruptible=False):
        super().__init__(name="fake", is_interruptible=is_interruptible)
        self._chunks = chunks
        self._raise = raise_exc

    async def generate_response(self):
        if self._raise is not None:
            raise self._raise
        for c in self._chunks:
            yield c


def _llm_request():
    return SDKSystemLLMRequestEvent(messages=[{"role": "user", "content": "hello"}])


def _names(events):
    return [type(e).__name__ for e in events]


def _fake_task_manager():
    """Task manager stub that does not run the background process loop (tests drive
    process_event directly). create_task closes the loop coroutine so it isn't left
    un-awaited; cancel_task is awaitable so the interrupt path works."""
    tm = mock.MagicMock()
    tm.create_task = lambda coro, *a, **k: (coro.close(), mock.MagicMock())[1]
    tm.cancel_task = mock.AsyncMock()
    return tm


class _CrewCase(unittest.IsolatedAsyncioTestCase):
    async def _started(self, node):
        """Start the node, record every event it emits, and stop it on cleanup."""
        recorded = []
        orig = node.send_event

        async def _rec(ev):
            recorded.append(ev)
            await orig(ev)

        node.send_event = _rec
        await node.start(mock.MagicMock(), _fake_task_manager())
        self.addAsyncCleanup(node.stop)
        return recorded


class CrewPremiseTest(_CrewCase):
    async def test_llm_request_drives_generate_response(self):
        """Seam: OutputCrewNode. LLM request -> start, chunks, end (the core turn)."""
        node = _FakeLLMNode(chunks=("Hi", " there"))
        rec = await self._started(node)
        await node.process_event(_llm_request())

        names = _names(rec)
        self.assertIn(SDKAgentLLMResponseStartEvent.__name__, names)
        self.assertIn(SDKAgentLLMResponseEndEvent.__name__, names)
        chunks = [e.text for e in rec if isinstance(e, SDKAgentLLMResponseChunkEvent)]
        self.assertEqual(chunks, ["Hi", " there"])
        self.assertLess(
            names.index(SDKAgentLLMResponseStartEvent.__name__),
            names.index(SDKAgentLLMResponseEndEvent.__name__),
        )

    async def test_speak_only_when_running(self):
        """Seam: speak(). Voices when running; no-ops (no event) when not."""
        node = _FakeLLMNode()
        rec = await self._started(node)
        await node.speak("live")
        self.assertTrue(any(isinstance(e, SDKAgentSpeakEvent) and e.text == "live" for e in rec))

        stopped = _FakeLLMNode()
        rec2 = []
        orig = stopped.send_event

        async def _rec(ev):
            rec2.append(ev)
            await orig(ev)

        stopped.send_event = _rec  # never started -> _running False
        await stopped.speak("dropped")
        self.assertFalse(any(isinstance(e, SDKAgentSpeakEvent) for e in rec2))

    async def test_failing_turn_surfaces_error_and_still_closes(self):
        """Edge case: generate_response raises -> fatal error event, End still sent."""
        node = _FakeLLMNode(raise_exc=RuntimeError("boom"))
        rec = await self._started(node)
        await node.process_event(_llm_request())

        names = _names(rec)
        self.assertIn(SDKAgentErrorEvent.__name__, names)
        self.assertIn(SDKAgentLLMResponseEndEvent.__name__, names)

    async def test_node_survives_interrupt_and_generates_after(self):
        """Edge case: barge-in. An interrupt must not break an interruptible node."""
        node = _FakeLLMNode(chunks=("after",), is_interruptible=True)
        rec = await self._started(node)
        await node.process_event(SDKSystemControlInterruptEvent())
        rec.clear()
        await node.process_event(_llm_request())
        chunks = [e.text for e in rec if isinstance(e, SDKAgentLLMResponseChunkEvent)]
        self.assertEqual(chunks, ["after"])


class CrewBackgroundNodeTest(_CrewCase):
    async def test_background_node_observes_without_speaking(self):
        """Seam: BackgroundCrewNode. Observes events, produces no user output."""

        class _Observer(BackgroundCrewNode):
            def __init__(self):
                super().__init__(name="obs")
                self.seen = []

            async def process_event(self, event):
                self.seen.append(event)
                await super().process_event(event)

        obs = _Observer()
        rec = await self._started(obs)
        await obs.process_event(_llm_request())

        self.assertTrue(obs.seen, "background node should observe the event")
        self.assertFalse(
            any(isinstance(e, (SDKAgentSpeakEvent, SDKAgentLLMResponseStartEvent)) for e in rec),
            "background node must not produce user-facing output",
        )


class CrewEventCodecTest(unittest.TestCase):
    def test_wire_round_trip_preserves_type_and_fields(self):
        """Seam: EventCodec. encode -> decode reconstructs the exact event subclass."""
        codec = EventCodec()
        for ev, field, val in (
            (SDKAgentSpeakEvent(text="hi"), "text", "hi"),
            (SDKAgentLLMResponseChunkEvent(text="chunk"), "text", "chunk"),
        ):
            decoded = codec.decode(json.loads(codec.encode(ev)))
            self.assertIsInstance(decoded, type(ev))
            self.assertEqual(getattr(decoded, field), val)


class CrewImportSeamTest(unittest.TestCase):
    def test_documented_imports_resolve(self):
        """Seam: imports. Every documented crew symbol imports (the customer's bug)."""
        from smallestai.atoms.crew import (  # noqa: F401
            AtomsCrewApp,
            BackgroundCrewNode,
            CrewSession,
            OpenAIClient,
            OutputCrewNode,
            ToolRegistry,
            function_tool,
        )


if __name__ == "__main__":
    unittest.main()
