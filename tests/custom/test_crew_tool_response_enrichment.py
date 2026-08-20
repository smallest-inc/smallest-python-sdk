"""A crew @function_tool that triggers a transfer/end-call but returns nothing
still gets a rich tool_call_end `response` (handoff summary), matching what
single-prompt agents surface — with no user code returning a dict.
"""

import asyncio

from smallestai.atoms.crew.clients.types import ToolCall
from smallestai.atoms.crew.events import (
    SDKAgentEndCallEvent,
    SDKAgentLogEvent,
    SDKAgentTransferConversationEvent,
    TransferOption,
    TransferOptionType,
    WarmTransferHandoffOptionType,
    WarmTransferPrivateHandoffOption,
)
from smallestai.atoms.crew.nodes import OutputCrewNode
from smallestai.atoms.crew.tools import ToolRegistry, function_tool


class _Node(OutputCrewNode):
    def __init__(self):
        super().__init__(name="t")
        self.sent = []
        self.registry = ToolRegistry()
        self.registry.discover(self)

    async def send_event(self, event):
        self.sent.append(event)
        await super().send_event(event)  # runs handoff latch + _pending_tool_response

    @function_tool(name="transfer_call")
    async def transfer_call(self) -> None:  # returns nothing, like the canonical example
        await self.send_event(
            SDKAgentTransferConversationEvent(
                transfer_call_number="+917900135795",
                transfer_options=TransferOption(
                    type=TransferOptionType.WARM_TRANSFER,
                    private_handoff_option=WarmTransferPrivateHandoffOption(
                        type=WarmTransferHandoffOptionType.PROMPT,
                        prompt="Brief the specialist on the caller's issue.",
                    ),
                ),
                on_hold_music="relaxing_sound",
            )
        )

    @function_tool(name="cold_transfer")
    async def cold_transfer(self) -> None:
        await self.send_event(
            SDKAgentTransferConversationEvent(
                transfer_call_number="+911234567890",
                transfer_options=TransferOption(type=TransferOptionType.COLD_TRANSFER),
            )
        )

    @function_tool(name="hang_up")
    async def hang_up(self) -> None:
        await self.send_event(SDKAgentEndCallEvent())

    @function_tool(name="noop")
    async def noop(self) -> None:
        return None


def _end_event(node, fn):
    for e in node.sent:
        if isinstance(e, SDKAgentLogEvent) and e.name == "tool_call_end" and e.payload["function_name"] == fn:
            return e
    return None


def test_transfer_tool_gets_handoff_response():
    node = _Node()
    asyncio.run(node.registry.execute([ToolCall(id="c1", name="transfer_call", arguments="{}")], parallel=False))
    resp = _end_event(node, "transfer_call").payload["context"]["response"]
    assert resp["status"] == "success"
    assert resp["action"] == "transfer_call"
    assert resp["transfer_number"] == "+917900135795"
    assert resp["transfer_type"] == TransferOptionType.WARM_TRANSFER.value
    # warm transfer includes the whisper briefing
    assert resp["private_handoff"]["type"] == WarmTransferHandoffOptionType.PROMPT.value
    assert "specialist" in resp["private_handoff"]["prompt"]


def test_cold_transfer_has_no_handoff():
    node = _Node()
    asyncio.run(node.registry.execute([ToolCall(id="c4", name="cold_transfer", arguments="{}")], parallel=False))
    resp = _end_event(node, "cold_transfer").payload["context"]["response"]
    assert resp["transfer_type"] == TransferOptionType.COLD_TRANSFER.value
    assert "private_handoff" not in resp and "public_handoff" not in resp


def test_end_call_tool_gets_handoff_response():
    node = _Node()
    asyncio.run(node.registry.execute([ToolCall(id="c2", name="hang_up", arguments="{}")], parallel=False))
    resp = _end_event(node, "hang_up").payload["context"]["response"]
    assert resp == {"status": "success", "action": "end_call"}


def test_plain_none_tool_has_no_response():
    # A tool that returns None and triggers no handoff stays as before (no response key).
    node = _Node()
    asyncio.run(node.registry.execute([ToolCall(id="c3", name="noop", arguments="{}")], parallel=False))
    ctx = _end_event(node, "noop").payload["context"]
    assert "response" not in ctx


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
