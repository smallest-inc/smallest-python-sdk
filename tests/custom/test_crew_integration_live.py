"""Live integration test for the crew premise — real LLM, no mocks.

Proves the code-first path works end to end against a real bring-your-own-LLM:
a real OutputCrewNode with a real OpenAIClient (pointed at Anthropic's
OpenAI-compatible endpoint) is driven by a real LLM-request event and must
stream a real, non-empty response, bracketed by Start/End and with no error.

Skipped unless ANTHROPIC_API_KEY is set, so the normal WireMock CI run skips it.
Run it live with:

    ANTHROPIC_API_KEY=sk-ant-... poetry run pytest tests/custom/test_crew_integration_live.py -m integration -s
"""

import os
import unittest
from unittest import mock

import pytest

pytestmark = pytest.mark.integration

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

from smallestai.atoms.crew.clients.openai import OpenAIClient  # noqa: E402
from smallestai.atoms.crew.events import (  # noqa: E402
    SDKAgentErrorEvent,
    SDKAgentLLMResponseChunkEvent,
    SDKAgentLLMResponseEndEvent,
    SDKAgentLLMResponseStartEvent,
    SDKSystemLLMRequestEvent,
)
from smallestai.atoms.crew.nodes import OutputCrewNode  # noqa: E402


class _LiveAgent(OutputCrewNode):
    def __init__(self):
        super().__init__(name="live")
        self.llm = OpenAIClient(
            model="claude-haiku-4-5",
            api_key=ANTHROPIC_API_KEY,
            base_url="https://api.anthropic.com/v1/",
        )

    async def generate_response(self):
        async for chunk in await self.llm.chat(self.context.messages, stream=True):
            if chunk.content:
                yield chunk.content


def _task_manager():
    tm = mock.MagicMock()
    tm.create_task = lambda coro, *a, **k: (coro.close(), mock.MagicMock())[1]
    tm.cancel_task = mock.AsyncMock()
    return tm


@unittest.skipUnless(ANTHROPIC_API_KEY, "ANTHROPIC_API_KEY not set; live crew test skipped")
class CrewLiveTurnTest(unittest.IsolatedAsyncioTestCase):
    async def test_real_llm_turn_streams_a_response(self):
        node = _LiveAgent()
        recorded = []
        orig = node.send_event

        async def _rec(ev):
            recorded.append(ev)
            await orig(ev)

        node.send_event = _rec
        await node.start(mock.MagicMock(), _task_manager())
        self.addAsyncCleanup(node.stop)

        node.context.add_message({"role": "system", "content": "You are terse."})
        await node.process_event(
            SDKSystemLLMRequestEvent(messages=[{"role": "user", "content": "Reply with exactly: hello from crew"}])
        )

        names = [type(e).__name__ for e in recorded]
        text = "".join(e.text for e in recorded if isinstance(e, SDKAgentLLMResponseChunkEvent))
        errors = [e for e in recorded if isinstance(e, SDKAgentErrorEvent)]

        self.assertEqual(errors, [], f"real turn errored: {[e.message for e in errors]}")
        self.assertIn(SDKAgentLLMResponseStartEvent.__name__, names)
        self.assertIn(SDKAgentLLMResponseEndEvent.__name__, names)
        self.assertTrue(text.strip(), "real LLM returned no text")


if __name__ == "__main__":
    unittest.main()
