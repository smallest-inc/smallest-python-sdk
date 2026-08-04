"""OutputCrewNode must stop generating after a handoff (transfer / end-call).

Regression: a crew @function_tool that emits a transfer/end-call event is
fire-and-forget (no tool_result recorded), so on every subsequent LLM request the
LLM re-decides the same action and re-fires the event / hold-message in a loop
(observed ~40x "please hold" during a ~30s transfer dial). Once a handoff event is
emitted, the node latches and ignores further LLM requests.
"""
import unittest
from unittest import mock

from smallestai.atoms.crew.nodes import OutputCrewNode
from smallestai.atoms.crew.events import (
    SDKSystemLLMRequestEvent,
    SDKAgentTransferConversationEvent,
    SDKAgentEndCallEvent,
    TransferOption,
    TransferOptionType,
)


class _Agent(OutputCrewNode):
    def __init__(self):
        super().__init__(name="a")

    async def generate_response(self):
        if False:
            yield ""


def _transfer_event():
    return SDKAgentTransferConversationEvent(
        transfer_call_number="+15551234567",
        transfer_options=TransferOption(type=TransferOptionType.COLD_TRANSFER),
    )


class TerminalHandoffGuardTest(unittest.IsolatedAsyncioTestCase):
    async def test_llm_requests_run_before_handoff(self):
        a = _Agent()
        a._handle_llm_request = mock.AsyncMock()
        a.send_event = mock.AsyncMock()  # base send_event isn't needed here
        await a.process_event(SDKSystemLLMRequestEvent(messages=[{"role": "user", "content": "hi"}]))
        a._handle_llm_request.assert_awaited_once()

    async def test_transfer_latches_and_suppresses_further_llm_requests(self):
        a = _Agent()
        a._handle_llm_request = mock.AsyncMock()
        # emit a transfer through the real send_event override (super().send_event is stubbed)
        with mock.patch.object(OutputCrewNode.__mro__[1], "send_event", new=mock.AsyncMock()):
            await a.send_event(_transfer_event())
        self.assertTrue(a._handoff_started)
        await a.process_event(SDKSystemLLMRequestEvent(messages=[{"role": "user", "content": "still there?"}]))
        a._handle_llm_request.assert_not_awaited()

    async def test_end_call_also_latches(self):
        a = _Agent()
        a._handle_llm_request = mock.AsyncMock()
        with mock.patch.object(OutputCrewNode.__mro__[1], "send_event", new=mock.AsyncMock()):
            await a.send_event(SDKAgentEndCallEvent())
        self.assertTrue(a._handoff_started)
        await a.process_event(SDKSystemLLMRequestEvent(messages=[{"role": "user", "content": "x"}]))
        a._handle_llm_request.assert_not_awaited()

    async def test_non_terminal_event_does_not_latch(self):
        a = _Agent()
        a._handle_llm_request = mock.AsyncMock()
        from smallestai.atoms.crew.events import SDKAgentSpeakEvent
        with mock.patch.object(OutputCrewNode.__mro__[1], "send_event", new=mock.AsyncMock()):
            await a.send_event(SDKAgentSpeakEvent(text="hello"))
        self.assertFalse(a._handoff_started)
        await a.process_event(SDKSystemLLMRequestEvent(messages=[{"role": "user", "content": "x"}]))
        a._handle_llm_request.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
