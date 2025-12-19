"""
Base client interface for LLM providers.

Defines the common interface that all LLM clients should implement.
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional, Union

from smallestai.atoms.agent.clients.types import ChatChunk, ChatResponse


class BaseLLMClient(ABC):
    """Base interface for LLM clients."""

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False,
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> Union[ChatResponse, AsyncIterator[ChatChunk]]:
        """
        Make a chat completion request.

        Args:
            messages: Chat messages in OpenAI format
            stream: Whether to stream response
            tools: Tool/function definitions
            **kwargs: Provider-specific parameters

        Returns:
            ChatResponse for non-streaming, AsyncIterator[ChatChunk] for streaming
        """
        pass

    @abstractmethod
    async def aclose(self):
        """Close client and cleanup resources."""
        pass
