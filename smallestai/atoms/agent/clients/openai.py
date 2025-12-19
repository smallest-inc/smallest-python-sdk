"""
OpenAI client implementation.

Standalone client for OpenAI and OpenAI-compatible APIs.
"""

import os
from typing import (
    Any,
    AsyncIterator,
    Dict,
    List,
    Literal,
    Optional,
    Union,
    overload,
)

import httpx
from dotenv import load_dotenv
from loguru import logger
from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
)

from smallestai.atoms.agent.clients.base import BaseLLMClient
from smallestai.atoms.agent.clients.types import ChatChunk, ChatResponse, ToolCall
from smallestai.atoms.agent.type import NOT_GIVEN, NotGivenOr, is_given

load_dotenv()


class OpenAIClient(BaseLLMClient):
    """
    Standalone OpenAI client for use in any node.

    Example:
        client = OpenAIClient(model="gpt-4o-mini")
        response = await client.chat(messages=[...])

        # Streaming
        async for chunk in client.chat(messages=[...], stream=True):
            print(chunk.content)

        # With tools
        response = await client.chat(
            messages=[...],
            tools=[{
                "type": "function",
                "function": {...}
            }]
        )
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: NotGivenOr[float] = NOT_GIVEN,
        max_tokens: NotGivenOr[int] = NOT_GIVEN,
        **kwargs: Any,
    ):
        """
        Initialize OpenAI client.

        Args:
            model: Model name (e.g., "gpt-4o-mini", "gpt-4")
            api_key: API key (or None to use OPENAI_API_KEY env var)
            base_url: Custom base URL for OpenAI-compatible APIs
            temperature: Default sampling temperature
            max_tokens: Default max completion tokens
            **kwargs: Additional default parameters
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._extra_kwargs = kwargs
        self._client = self._create_client(api_key, base_url)

    def _create_client(
        self, api_key: Optional[str], base_url: Optional[str]
    ) -> AsyncOpenAI:
        """Create the OpenAI async client."""
        # Get API key from parameter or environment
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning(
                "No OpenAI API key provided. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        # Create httpx client with connection pooling
        http_client = httpx.AsyncClient(
            limits=httpx.Limits(
                max_keepalive_connections=100,
                max_connections=1000,
            )
        )

        # Create OpenAI client
        client_kwargs: Dict[str, Any] = {
            "api_key": api_key,
            "http_client": http_client,
        }

        if base_url:
            client_kwargs["base_url"] = base_url

        return AsyncOpenAI(**client_kwargs)

    def _build_params(
        self,
        messages: List[Dict[str, Any]],
        stream: bool,
        tools: Optional[List[Dict[str, Any]]],
        overrides: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build parameters for OpenAI API call."""
        params: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
        }

        if stream:
            params["stream_options"] = {"include_usage": True}

        temperature = overrides.get("temperature")
        if temperature is not None:
            params["temperature"] = temperature
        elif is_given(self.temperature):
            params["temperature"] = self.temperature

        # Add max_tokens if set
        max_tokens = overrides.get("max_tokens")
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        elif is_given(self.max_tokens):
            params["max_tokens"] = self.max_tokens

        # Add tools if provided
        if tools:
            params["tools"] = tools

        # Merge extra_kwargs
        for key, value in self._extra_kwargs.items():
            if key not in params:
                params[key] = value

        for key, value in overrides.items():
            if key not in ["temperature", "max_tokens", "tools"] and value is not None:
                params[key] = value

        return params

    @overload
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        stream: Literal[False],
        tools: Optional[List[Dict[str, Any]]] = None,
        **overrides: Any,
    ) -> ChatResponse: ...

    @overload
    async def chat(
        self,
        messages: List[Dict[str, Any]],
        stream: Literal[True],
        tools: Optional[List[Dict[str, Any]]] = None,
        **overrides: Any,
    ) -> AsyncIterator[ChatChunk]: ...

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False,
        tools: Optional[List[Dict[str, Any]]] = None,
        **overrides: Any,
    ) -> Union[ChatResponse, AsyncIterator[ChatChunk]]:
        """
        Make a chat completion request.

        Args:
            messages: Chat messages in OpenAI format
            stream: Whether to stream response
            tools: Tool/function definitions
            **overrides: Per-request parameter overrides

        Returns:
            ChatResponse for non-streaming, AsyncIterator[ChatChunk] for streaming

        Example:
            # Non-streaming
            response = await client.chat(messages=[...])
            print(response.content)

            # Streaming
            async for chunk in client.chat(messages=[...], stream=True):
                if chunk.content:
                    print(chunk.content, end="")
        """
        params = self._build_params(messages, stream, tools, overrides)

        logger.debug(
            f"OpenAI chat request: model={params['model']}, "
            f"messages={len(params['messages'])}, stream={stream}"
        )

        if stream:
            return self._stream_completion(params)
        else:
            return await self._complete(params)

    async def _stream_completion(
        self, params: Dict[str, Any]
    ) -> AsyncIterator[ChatChunk]:
        """Stream chat completion chunks."""
        functions_list = []
        arguments_list = []
        tool_id_list = []
        func_idx = 0
        function_name = ""
        arguments = ""
        tool_call_id = ""

        stream: AsyncStream[
            ChatCompletionChunk
        ] = await self._client.chat.completions.create(**params)

        async for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            finish_reason = chunk.choices[0].finish_reason

            content = delta.content if delta.content else None

            if delta.tool_calls:
                tool_call = delta.tool_calls[0]
                if tool_call.index != func_idx:
                    functions_list.append(function_name)
                    arguments_list.append(arguments)
                    tool_id_list.append(tool_call_id)
                    function_name = ""
                    arguments = ""
                    tool_call_id = ""
                    func_idx += 1
                if tool_call.function and tool_call.function.name:
                    function_name += tool_call.function.name
                    tool_call_id = tool_call.id
                if tool_call.function and tool_call.function.arguments:
                    arguments += tool_call.function.arguments

            yield ChatChunk(
                content=content, tool_calls=None, finish_reason=finish_reason
            )

        if function_name:
            functions_list.append(function_name)
            arguments_list.append(arguments)
            tool_id_list.append(tool_call_id)

        if functions_list:
            tool_calls = [
                ToolCall(
                    id=tool_id,
                    name=function_name,
                    arguments=arguments,
                )
                for tool_id, function_name, arguments in zip(
                    tool_id_list, functions_list, arguments_list
                )
            ]
            yield ChatChunk(
                content=None, tool_calls=tool_calls, finish_reason=finish_reason
            )

    async def _complete(self, params: Dict[str, Any]) -> ChatResponse:
        """Non-streaming completion."""
        response: ChatCompletion = await self._client.chat.completions.create(**params)

        if not response.choices:
            return ChatResponse(content=None, tool_calls=None, usage=None)

        message = response.choices[0].message

        # Extract content
        content = message.content

        tool_calls: List[ToolCall] = []
        if message.tool_calls:
            for i in message.tool_calls:
                if i.type == "function":
                    tool_calls.append(
                        ToolCall(
                            id=i.id,
                            name=i.function.name,
                            arguments=i.function.arguments,
                        )
                    )
                elif i.type == "custom":
                    tool_calls.append(
                        ToolCall(
                            id=i.id,
                            name=i.custom.name,
                            arguments=i.custom.input,
                        )
                    )

        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        return ChatResponse(content=content, tool_calls=tool_calls, usage=usage)

    async def aclose(self):
        """Close the OpenAI client and cleanup resources."""
        if self._client:
            await self._client.close()
