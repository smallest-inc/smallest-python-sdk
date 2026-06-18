"""
Base client interface for LLM providers.

Defines the common interface that all LLM clients should implement.
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Literal, Optional, Union, overload

from smallestai.atoms.crew.clients.types import ChatChunk, ChatResponse


class BaseLLMClient(ABC):
    """Base interface for LLM clients."""

    @overload
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        stream: Literal[False] = ...,
        tools: Optional[List[Dict[str, Any]]] = ...,
        **kwargs: Any,
    ) -> ChatResponse: ...

    @overload
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        stream: Literal[True] = ...,
        tools: Optional[List[Dict[str, Any]]] = ...,
        **kwargs: Any,
    ) -> AsyncIterator[ChatChunk]: ...

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
