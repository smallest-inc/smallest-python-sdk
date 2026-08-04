"""
Agent-crew node that transfers the call, with a custom LLM — smallestai 5.4.0.

In an agent crew, a transfer is code: a node emits SDKAgentTransferConversationEvent.
This is the node you'd ship in a crew project (server.py registers the crew and
`smallestai agent-crew deploy` builds it). Shown with a custom LLM (any OpenAI-
compatible endpoint — here Anthropic/Claude) to mirror a common setup.

Key points this example bakes in:
  - The node's generate_response uses self.context.messages, which the SDK now
    seeds from the platform's authoritative LLM-request messages (5.4.0) — so the
    agent always sees the latest user turn and doesn't go silent.
  - The system prompt must clearly tell the LLM WHEN to call transfer_call.
  - on_hold_music applies to warm_transfer only; cold_transfer is a direct connect.

Deploy (from a project dir with this file as the node, a server.py, and a
requirements.txt pinning smallestai>=5.4.0 plus your LLM client):
    smallestai agent-crew deploy --entry-point server.py
"""
import os

from smallestai.atoms.crew.nodes import OutputCrewNode
from smallestai.atoms.crew.events import (
    SDKAgentTransferConversationEvent,
    TransferOption,
    TransferOptionType,
)

# Bring your own OpenAI-compatible client + tool registry. This example assumes a
# client exposing `.chat(messages=..., stream=True, tools=...)` and a registry that
# turns @function_tool methods into schemas; wire in whatever your crew uses.
# (Guarded so this template file imports cleanly; replace with your real client.)
try:
    from your_llm import OpenAIClient, ToolRegistry, function_tool  # type: ignore
except ImportError:  # template placeholder
    OpenAIClient = ToolRegistry = None

    def function_tool(name):  # type: ignore
        def _decorator(fn):
            return fn

        return _decorator

TRANSFER_NUMBER = os.getenv("TRANSFER_CALL_NUMBER", "+15551234567")


class Assistant(OutputCrewNode):
    def __init__(self) -> None:
        super().__init__(name="assistant")
        self.llm = OpenAIClient(
            model=os.getenv("CUSTOM_LLM_MODEL", "claude-haiku-4-5"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            base_url=os.getenv("CUSTOM_LLM_BASE_URL", "https://api.anthropic.com/v1/"),
        )
        # System prompt: be explicit about when to transfer, or the tool never fires.
        self.context.add_message(
            {
                "role": "system",
                "content": (
                    "You are Acme support. The moment the caller asks for a human, a "
                    "person, a specialist, or to be transferred, call the transfer_call "
                    "tool immediately. Do not keep talking — just call the tool."
                ),
            }
        )
        self.tool_registry = ToolRegistry()
        self.tool_registry.discover(self)
        self.tool_schemas = self.tool_registry.get_schemas()

    @function_tool(name="transfer_call")
    async def transfer_call(self) -> None:
        """Transfer the call to a human specialist."""
        await self.send_event(
            SDKAgentTransferConversationEvent(
                transfer_call_number=TRANSFER_NUMBER,
                # cold = direct connect; use WARM_TRANSFER + on_hold_music for music.
                transfer_options=TransferOption(type=TransferOptionType.COLD_TRANSFER),
                # on_hold_music="relaxing_sound",  # warm transfer only
            )
        )

    async def generate_response(self):
        # self.context.messages is seeded from the platform's authoritative
        # messages before this runs (5.4.0), so it always has the latest user turn.
        response = await self.llm.chat(
            messages=self.context.messages, stream=True, tools=self.tool_schemas
        )
        full = ""
        tool_calls = []
        async for chunk in response:
            if chunk.content:
                full += chunk.content
                yield chunk.content
            if chunk.tool_calls:
                tool_calls.extend(chunk.tool_calls)
        if tool_calls:
            await self.tool_registry.execute(tool_calls=tool_calls, parallel=True)
            return
        if full:
            self.context.add_message({"role": "assistant", "content": full})
