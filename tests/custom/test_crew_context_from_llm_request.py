"""OutputCrewNode must seed its context from the LLM-request event's messages.

Regression: the crew relied only on separately-accumulated transcript events to
populate self.context. When those raced the LLM request or were dropped, the
context was empty, Claude 400'd ("no non-system message"), and the agent went
silent for the whole call. The LLM-request event carries the platform's
authoritative message list, so we seed the context from it before generating.
"""
import unittest
from unittest import mock

from smallestai.atoms.crew.nodes import OutputCrewNode
from smallestai.atoms.crew.events import SDKSystemLLMRequestEvent, SDKAgentTranscriptUpdateEvent


class _Agent(OutputCrewNode):
    def __init__(self):
        super().__init__(name="a")

    async def generate_response(self):
        if False:
            yield ""


class ContextFromLLMRequestTest(unittest.IsolatedAsyncioTestCase):
    async def test_context_seeded_from_event_messages(self):
        agent = _Agent()
        agent.send_event = mock.AsyncMock()
        msgs = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "transfer me to a human"},
        ]
        await agent.process_event(SDKSystemLLMRequestEvent(messages=msgs))
        # generate_response would now see the authoritative context, incl. the user turn
        assert agent.context.messages == msgs

    async def test_empty_context_is_populated_before_generation(self):
        """The exact silence bug: no transcript events arrived, but the request
        carries the messages, so the context is non-empty when we generate."""
        agent = _Agent()
        agent.send_event = mock.AsyncMock()
        seen = {}

        async def fake_handle():
            seen["had_user"] = any(m.get("role") == "user" for m in agent.context.messages)

        agent._handle_llm_request = fake_handle
        await agent.process_event(
            SDKSystemLLMRequestEvent(messages=[{"role": "user", "content": "hi"}])
        )
        assert seen["had_user"] is True

    async def test_no_messages_falls_back_to_accumulated_context(self):
        """Backward compat: a request without messages leaves accumulated context intact."""
        agent = _Agent()
        agent.send_event = mock.AsyncMock()
        await agent.process_event(SDKAgentTranscriptUpdateEvent(role="user", content="hello"))
        await agent.process_event(SDKSystemLLMRequestEvent())  # no messages
        assert agent.context.messages == [{"role": "user", "content": "hello"}]

    async def test_node_system_prompt_is_preserved(self):
        """A crew sets its system prompt in code; syncing from the event must keep it."""
        agent = _Agent()
        agent.send_event = mock.AsyncMock()
        agent.context.add_message({"role": "system", "content": "CREW SYSTEM PROMPT"})
        await agent.process_event(
            SDKSystemLLMRequestEvent(messages=[{"role": "user", "content": "hi"}])
        )
        assert agent.context.messages == [
            {"role": "system", "content": "CREW SYSTEM PROMPT"},
            {"role": "user", "content": "hi"},
        ]

    async def test_event_messages_are_authoritative_over_stale_accumulation(self):
        agent = _Agent()
        agent.send_event = mock.AsyncMock()
        await agent.process_event(SDKAgentTranscriptUpdateEvent(role="user", content="stale"))
        fresh = [{"role": "user", "content": "fresh authoritative turn"}]
        await agent.process_event(SDKSystemLLMRequestEvent(messages=fresh))
        assert agent.context.messages == fresh


    async def test_empty_list_messages_keeps_accumulated_context(self):
        """A request whose messages is [] must not wipe context to a system-only list."""
        agent = _Agent()
        agent.send_event = mock.AsyncMock()
        agent.context.add_message({"role": "system", "content": "SYS"})
        await agent.process_event(SDKAgentTranscriptUpdateEvent(role="user", content="hello"))
        await agent.process_event(SDKSystemLLMRequestEvent(messages=[]))
        assert agent.context.messages == [
            {"role": "system", "content": "SYS"},
            {"role": "user", "content": "hello"},
        ]

    async def test_system_only_event_does_not_clobber_conversation(self):
        """If the event carries only a system message, keep the existing conversation."""
        agent = _Agent()
        agent.send_event = mock.AsyncMock()
        agent.context.add_message({"role": "system", "content": "SYS"})
        agent.context.add_message({"role": "user", "content": "earlier turn"})
        await agent.process_event(SDKSystemLLMRequestEvent(messages=[{"role": "system", "content": "S2"}]))
        assert {"role": "user", "content": "earlier turn"} in agent.context.messages

    async def test_tool_call_sequence_order_preserved(self):
        """assistant(tool_calls) + tool(result) survive the sync in order."""
        agent = _Agent()
        agent.send_event = mock.AsyncMock()
        msgs = [
            {"role": "system", "content": "SYS"},
            {"role": "user", "content": "transfer me"},
            {"role": "assistant", "content": "", "tool_calls": [{"id": "t1", "function": {"name": "transfer_call"}}]},
            {"role": "tool", "tool_call_id": "t1", "content": "ok"},
            {"role": "user", "content": "thanks"},
        ]
        await agent.process_event(SDKSystemLLMRequestEvent(messages=msgs))
        assert agent.context.messages == msgs  # order + tool block intact


if __name__ == "__main__":
    unittest.main()
