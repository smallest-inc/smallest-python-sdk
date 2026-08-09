"""
OutputCrewNode - Base class for agents that produce user-facing output.

Features:
- Automatically handles CONTROL_INTERRUPT
- Cancels streaming on interrupt
- Emits LLM_RESPONSE_START/CHUNK/END events
- Subclass implements generate_response()
"""

import traceback as _traceback
from abc import abstractmethod
from typing import Any, AsyncIterator, Dict

from loguru import logger

from smallestai.atoms.crew.context import ContextManager
from smallestai.atoms.crew.events import (
    OutputAgentSettings,
    SDKAgentEndCallEvent,
    SDKAgentErrorEvent,
    SDKAgentLLMResponseChunkEvent,
    SDKAgentLLMResponseEndEvent,
    SDKAgentLLMResponseStartEvent,
    SDKAgentSpeakEvent,
    SDKAgentTranscriptUpdateEvent,
    SDKAgentTransferConversationEvent,
    SDKEvent,
    SDKSystemInitEvent,
    SDKSystemLLMRequestEvent,
    SDKSystemUpdateOutputAgentSettingsEvent,
)

# Events that hand the call off / end it. Once one is emitted the conversation is
# over for this node, so we stop responding to further LLM requests.
_HANDOFF_EVENTS = (SDKAgentTransferConversationEvent, SDKAgentEndCallEvent)
from smallestai.atoms.crew.nodes.base import CrewNode
from smallestai.atoms.crew.task_manager import TaskManager


class OutputCrewNode(CrewNode):
    """
    Base class for agents that produce user-facing output.

    This node type:
    - Automatically handles CONTROL_INTERRUPT events
    - Cancels any ongoing generation when interrupted
    - Emits LLM_RESPONSE_START/CHUNK/END events automatically
    - Is designed for voice agents, chatbots, and other interactive agents

    Usage:
        class MyVoiceAgent(OutputCrewNode):
            def __init__(self):
                super().__init__(name="voice-agent")
                self.llm = OpenAIClient(model="gpt-4o-mini")

            async def generate_response(self, messages):
                async for chunk in self.llm.chat(messages, stream=True):
                    if chunk.content:
                        yield chunk.content
    """

    def __init__(self, name: str, is_interruptible: bool = True):
        """
        Initialize output agent node.

        Args:
            name: CrewNode name
        """
        super().__init__(name, is_interruptible)
        self.settings = OutputAgentSettings()
        self.context = ContextManager()
        # Latched once a handoff (transfer / end-call) event is emitted. After a
        # handoff there is nothing to generate, and generating anyway causes a
        # feedback loop: a tool that emits the event is fire-and-forget (no
        # tool_result is recorded), so the LLM keeps re-deciding the same action
        # on every subsequent request — repeatedly re-firing the event / speech.
        self._handoff_started = False

    async def start(self, init_event: SDKSystemInitEvent, task_manager: TaskManager):
        """Start the node"""
        await super().start(init_event, task_manager)

    async def send_event(self, event: SDKEvent):
        """Emit an event, latching handoff state so we stop generating after a
        transfer / end-call. Preserves base behavior otherwise."""
        if isinstance(event, _HANDOFF_EVENTS):
            self._handoff_started = True
        await super().send_event(event)

    async def _update_settings(self, settings: Dict[str, Any]):
        """Update the settings for this node"""
        for key, value in settings.items():
            logger.debug(f"[{self.name}] Updating setting {key} to {value}")
            setattr(self.settings, key, value)

    async def _route_framework_event(self, event: SDKEvent):
        """Framework-owned event routing. Always runs, independent of any user
        `on_event` override, so a subclass can't accidentally silence the agent
        (e.g. by dropping the LLM-request -> generate_response path)."""
        if isinstance(event, SDKSystemLLMRequestEvent):
            # After a handoff (transfer / end-call) there is nothing to generate;
            # ignore further LLM requests so the node doesn't re-decide and
            # re-fire the same terminal action in a loop.
            if self._handoff_started:
                return
            # The LLM-request event carries the platform's authoritative message
            # list. Sync the user/assistant conversation from it so
            # generate_response always sees the latest user turn, instead of
            # relying only on separately-accumulated transcript events — those can
            # race the request or be dropped, leaving the context empty (Claude
            # then 400s on "no non-system message" and the agent goes silent).
            #
            # The node's own system prompt(s) are preserved: a crew sets its system
            # message in code (self.context.add_message), and the platform's list
            # may not carry it. Fall back to the accumulated context when a request
            # carries no messages.
            if event.messages:
                system_msgs = [m for m in self.context.messages if m.get("role") == "system"]
                if not system_msgs:
                    system_msgs = [m for m in event.messages if m.get("role") == "system"]
                conversation = [m for m in event.messages if m.get("role") != "system"]
                # Only sync when the request actually carries a conversation. If it
                # carries only a system message (or is otherwise empty of turns),
                # keep the accumulated context rather than shipping a system-only
                # list, which would re-introduce the "no non-system message" 400.
                if conversation:
                    self.context.set_messages(system_msgs + conversation)
            await self._handle_llm_request()
        elif isinstance(event, SDKAgentTranscriptUpdateEvent):
            self.context.add_message({"role": event.role, "content": event.content})
        elif isinstance(event, SDKSystemUpdateOutputAgentSettingsEvent):
            await self._update_settings(event.settings)

    async def on_event(self, event: SDKEvent):
        """Override this to react to events. This is the safe extension point:
        the framework routing (interrupts, LLM requests, transcript/context and
        settings updates) already ran before this is called, so you do NOT need
        to call super(). Prefer this over overriding `process_event`, which
        carries that framework routing — dropping it silences the agent."""
        pass

    async def process_event(self, event: SDKEvent):
        """Framework dispatch: interrupt handling, output-node routing, the user
        `on_event` hook, then forward. Prefer overriding `on_event` over this."""
        await super().process_event(event)
        await self._route_framework_event(event)
        await self.on_event(event)
        await self.send_event(event)

    async def speak(self, text: str):
        """Send the given text"""

        if not self._running:
            logger.warning(f"[{self.name}] Not running, cannot send message")
            return

        await self.send_event(SDKAgentSpeakEvent(text=text))

    async def _handle_llm_request(self):
        """
        Handle LLM request by starting response generation.

        Cancels any existing generation task before starting new one.
        """
        try:
            await self.send_event(SDKAgentLLMResponseStartEvent())

            async for chunk in self.generate_response():
                chunk_event = SDKAgentLLMResponseChunkEvent(text=chunk)
                await self.send_event(chunk_event)

        except Exception as e:
            logger.exception(f"[{self.name}] Error during generation: {e}")
            await self.send_event(
                SDKAgentErrorEvent(
                    message=f"{type(e).__name__} in {self.name}.generate_response: {e}",
                    severity="fatal",
                    payload={
                        "node_name": self.name,
                        "error_class": type(e).__name__,
                        "traceback": _traceback.format_exc(),
                    },
                )
            )

        finally:
            await self.send_event(SDKAgentLLMResponseEndEvent())
            logger.debug(f"[{self.name}] Generation completed")

    @abstractmethod
    async def generate_response(self) -> AsyncIterator[str]:
        """
        Generate response chunks (implement in subclass).

        This is where you call your LLM client and yield text chunks.

        Args:
            messages: Conversation messages

        Yields:
            Text chunks to stream

        Example:
            async def generate_response(self, messages):
                async for chunk in self.llm.chat(messages, stream=True):
                    if chunk.content:
                        yield chunk.content
        """
        pass
