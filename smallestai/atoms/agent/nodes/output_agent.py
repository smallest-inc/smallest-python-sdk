"""
OutputAgentNode - Base class for agents that produce user-facing output.

Features:
- Automatically handles CONTROL_INTERRUPT
- Cancels streaming on interrupt
- Emits LLM_RESPONSE_START/CHUNK/END events
- Subclass implements generate_response()
"""

from abc import abstractmethod
from typing import Any, AsyncIterator, Dict

from loguru import logger

from smallestai.atoms.agent.context import ContextManager
from smallestai.atoms.agent.events import (
    OutputAgentSettings,
    SDKAgentErrorEvent,
    SDKAgentLLMResponseChunkEvent,
    SDKAgentLLMResponseEndEvent,
    SDKAgentLLMResponseStartEvent,
    SDKAgentSpeakEvent,
    SDKAgentTranscriptUpdateEvent,
    SDKEvent,
    SDKSystemInitEvent,
    SDKSystemLLMRequestEvent,
    SDKSystemUpdateOutputAgentSettingsEvent,
)
from smallestai.atoms.agent.nodes.base import Node
from smallestai.atoms.agent.task_manager import TaskManager


class OutputAgentNode(Node):
    """
    Base class for agents that produce user-facing output.

    This node type:
    - Automatically handles CONTROL_INTERRUPT events
    - Cancels any ongoing generation when interrupted
    - Emits LLM_RESPONSE_START/CHUNK/END events automatically
    - Is designed for voice agents, chatbots, and other interactive agents

    Usage:
        class MyVoiceAgent(OutputAgentNode):
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
            name: Node name
        """
        super().__init__(name, is_interruptible)
        self.settings = OutputAgentSettings()
        self.context = ContextManager()

    async def start(self, init_event: SDKSystemInitEvent, task_manager: TaskManager):
        """Start the node"""
        await super().start(init_event, task_manager)

    async def _update_settings(self, settings: Dict[str, Any]):
        """Update the settings for this node"""
        for key, value in settings.items():
            logger.debug(f"[{self.name}] Updating setting {key} to {value}")
            setattr(self.settings, key, value)

    async def process_event(self, event: SDKEvent):
        """
        Route events to appropriate handlers.

        Handles:
        - LLMRequestEvent -> Start generation
        """

        await super().process_event(event)

        if isinstance(event, SDKSystemLLMRequestEvent):
            await self._handle_llm_request()
        elif isinstance(event, SDKAgentTranscriptUpdateEvent):
            self.context.add_message({"role": event.role, "content": event.content})
        elif isinstance(event, SDKSystemUpdateOutputAgentSettingsEvent):
            await self._update_settings(event.settings)

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
            error_event = SDKAgentErrorEvent(
                message=str(e),
            )
            await self.send_event(error_event)

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
