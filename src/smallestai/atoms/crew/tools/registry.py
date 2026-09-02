"""
Tool registry with automatic execution.

Manages registration and execution of function tools.
"""

import asyncio
import inspect
import json
from typing import Any, Callable, Dict, List, Optional, Union

from loguru import logger

from smallestai.atoms.crew.clients.types import ToolCall, ToolResult
from smallestai.atoms.crew.tools.decorator import (
    FunctionToolInfo,
    find_function_tools,
    is_function_tool,
)


class ToolRegistry:
    """
    Registry for managing and executing tools.

    Example:
        registry = ToolRegistry()

        @function_tool
        async def get_weather(location: str):
            return {"temp": 75}

        registry.register(get_weather)

        # Get schemas for LLM
        schemas = registry.get_schemas()

        # Execute tool calls from LLM
        results = await registry.execute(tool_calls)
    """

    def __init__(self):
        """Initialize empty registry."""
        self._tools: Dict[str, FunctionToolInfo] = {}
        # Set by discover() to the owning crew node. When present, tool
        # executions emit tool_call_start/end/error events over the node's
        # websocket so the platform surfaces them on the call's Events tab
        # (the same tool-call events single-prompt agents already show).
        self._owner: Any = None

    def register(self, func_or_info: Union[Callable, FunctionToolInfo]):
        """
        Register a @function_tool decorated function.

        Args:
            func: Function decorated with @function_tool

        Raises:
            ValueError: If function is not decorated

        Example:
            @function_tool
            async def my_tool(param: str):
                return "result"

            registry.register(my_tool)
        """

        if isinstance(func_or_info, FunctionToolInfo):
            self._tools[func_or_info.name] = func_or_info
            return

        if not is_function_tool(func_or_info):
            raise ValueError(
                f"{func_or_info.__name__} is not decorated with @function_tool. "
                f"Use @function_tool decorator before registering."
            )

        info: FunctionToolInfo = func_or_info.__tool_info__  # type: ignore

        # If the function is a class method then it will be bound to a class instance
        # but when using the decorator it runs before the class instance is created
        # so we need to bind the function to the class instance
        if inspect.ismethod(func_or_info):
            info = FunctionToolInfo(
                name=info.name,
                description=info.description,
                schema=info.schema,
                function=func_or_info,
            )

        self._tools[info.name] = info
        logger.debug(f"Registered tool: {info.name}")

    def discover(self, obj: Any):
        """
        Auto-discover and register all @function_tool methods in object.

        Args:
            obj: Object to scan for decorated methods

        Example:
            class MyAgent:
                @function_tool
                async def tool1(self): pass

                @function_tool
                async def tool2(self): pass

            agent = MyAgent()
            registry.discover(agent)  # Registers both tools
        """
        self._owner = obj
        tools = find_function_tools(obj)
        for tool in tools:
            self.register(tool)

    def get_schemas(self) -> List[Dict[str, Any]]:
        """
        Get OpenAI-compatible tool schemas.

        Returns:
            List of tool schemas for LLM

        Example:
            schemas = registry.get_schemas()
            response = await llm.chat(messages=[...], tools=schemas)
        """
        return [{"type": "function", "function": tool.schema.to_dict()} for tool in self._tools.values()]

    async def execute(
        self,
        tool_calls: List[ToolCall],
        context: Optional[Any] = None,
        parallel: bool = True,
    ) -> List[ToolResult]:
        """
        Execute tool calls automatically.

        Args:
            tool_calls: List of tool calls from LLM
            context: Optional context to pass to tools
            parallel: Execute tools in parallel (True) or sequential (False)

        Returns:
            List of tool results to send back to LLM

        Example:
            # LLM returns tool calls
            response = await llm.chat(...)
            if response.tool_calls:
                results = await registry.execute(response.tool_calls)
                # Send results back to LLM
                messages.extend([r.to_message() for r in results])
        """
        if parallel:
            return await self._execute_parallel(tool_calls, context)
        else:
            return await self._execute_sequential(tool_calls, context)

    async def _execute_parallel(self, tool_calls: List[ToolCall], context: Optional[Any]) -> List[ToolResult]:
        """Execute all tools in parallel."""
        tasks = [self._execute_single(call, context) for call in tool_calls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle exceptions
        final_results: List[ToolResult] = []
        for result in results:
            if isinstance(result, BaseException):
                # Create error result
                logger.exception(f"Tool execution failed: {result}")
                final_results.append(
                    ToolResult(
                        tool_call_id="",
                        name="",
                        content=str(result),
                        is_error=True,
                    )
                )
            else:
                final_results.append(result)

        return final_results

    async def _execute_sequential(self, tool_calls: List[ToolCall], context: Optional[Any]) -> List[ToolResult]:
        """Execute tools one by one."""
        results = []
        for call in tool_calls:
            result = await self._execute_single(call, context)
            results.append(result)
        return results

    async def _emit_tool_event(
        self,
        name: str,
        call: ToolCall,
        arguments: Any,
        *,
        response: Any = None,
        error: Optional[str] = None,
        latency_ms: int = 0,
        success: bool = True,
    ) -> None:
        """Emit a tool_call_start/end/error event over the owning node's websocket.

        No-op when the registry isn't owned by a crew node (standalone use) or
        the node can't send events. Observability must never break tool
        execution, so all failures here are swallowed.
        """
        send = getattr(self._owner, "send_event", None)
        if send is None or not asyncio.iscoroutinefunction(send):
            return

        context: Dict[str, Any] = {"arguments": arguments}
        if response is not None:
            try:
                json.dumps(response)
                context["response"] = response
            except (TypeError, ValueError):
                context["response"] = str(response)

        payload: Dict[str, Any] = {
            "turn_id": "",
            "tool_call_id": call.id,
            "function_name": call.name,
            "context": context,
        }
        if name == "tool_call_end":
            payload["latency"] = latency_ms
            payload["success"] = success
        elif name == "tool_call_error":
            payload["error"] = error
            payload["success"] = False

        try:
            from smallestai.atoms.crew.events import SDKAgentLogEvent

            await send(SDKAgentLogEvent(name=name, payload=payload))
        except Exception as exc:  # never let telemetry break a tool
            logger.debug(f"tool-call event emit skipped ({name}): {exc}")

    async def _execute_single(self, call: ToolCall, context: Optional[Any]) -> ToolResult:
        """Execute a single tool call."""
        import time

        started = time.monotonic()
        arguments: Any = {}
        try:
            tool_info = self._tools.get(call.name)
            if not tool_info:
                raise ValueError(f"Unknown tool: {call.name}")

            arguments = json.loads(call.arguments)

            await self._emit_tool_event("tool_call_start", call, arguments)

            # Clear any handoff summary so it reflects only this tool's effects.
            if hasattr(self._owner, "_pending_tool_response"):
                self._owner._pending_tool_response = None

            func = tool_info.function
            args, kwargs = self._prepare_arguments(func, arguments, context)

            logger.debug(f"Executing tool: {call.name} with args={args}, kwargs={kwargs}")

            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if isinstance(result, (dict, list, str, int, float, bool, type(None))):
                content = json.dumps(result)
            else:
                content = str(result)

            logger.debug(f"Tool {call.name} completed successfully")

            # If the tool returned nothing but triggered a handoff (transfer /
            # end-call) via the node, surface the handoff summary as the event's
            # response — so the platform shows the same detail single-prompt does,
            # without the user having to return it. Only enriches the event; the
            # tool's own return value (and the LLM-facing result) is unchanged.
            event_response = result
            if result is None:
                side_effect = getattr(self._owner, "_pending_tool_response", None)
                if side_effect:
                    event_response = side_effect

            await self._emit_tool_event(
                "tool_call_end",
                call,
                arguments,
                response=event_response,
                latency_ms=int((time.monotonic() - started) * 1000),
                success=True,
            )

            return ToolResult(
                tool_call_id=call.id,
                name=call.name,
                content=content,
                is_error=False,
            )

        except Exception as e:
            logger.exception(f"Error executing tool {call.name}: {e}")
            await self._emit_tool_event(
                "tool_call_error",
                call,
                arguments,
                error=str(e),
                latency_ms=int((time.monotonic() - started) * 1000),
                success=False,
            )
            return ToolResult(
                tool_call_id=call.id,
                name=call.name,
                content=str(e),
                is_error=True,
            )

    def _prepare_arguments(
        self, func: Callable, arguments: Dict[str, Any], context: Optional[Any]
    ) -> tuple[List[Any], Dict[str, Any]]:
        """
        Prepare function arguments, injecting context if needed.

        Args:
            func: Function to call
            arguments: Arguments from LLM
            context: Optional context to inject

        Returns:
            Tuple of (args, kwargs)
        """
        signature = inspect.signature(func)
        args: List[Any] = []
        kwargs: Dict[str, Any] = {}

        for param_name, param in signature.parameters.items():
            if param_name in ("self", "cls"):
                continue

            # TODO: Support context injection via type hints
            # For now, just use arguments from LLM
            if param_name in arguments:
                kwargs[param_name] = arguments[param_name]

        return args, kwargs
