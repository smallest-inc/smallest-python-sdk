"""
Function tool decorator.

Provides @function_tool decorator for marking functions as tools.
"""

import inspect
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from smallestai.atoms.agent.tools.schema import FunctionSchema, extract_function_schema


@dataclass
class FunctionToolInfo:
    """Metadata for a function tool."""

    name: str
    description: str
    schema: FunctionSchema
    function: Callable


def function_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Callable:
    """
    Decorator to mark a function as a tool.

    Auto-extracts schema from:
    - Function signature and type hints
    - Docstring (Google/NumPy format)
    - Annotated types with Field descriptions

    Args:
        name: Override function name
        description: Override description

    Returns:
        Decorated function with __tool_info__ attribute

    Example:
        @function_tool
        async def get_weather(location: str, format: str = "celsius"):
            '''Get current weather.

            Args:
                location: City and state
                format: Temperature format (celsius/fahrenheit)
            '''
            return {"temp": 75, "conditions": "sunny"}

        # Function now has __tool_info__ attribute
        assert hasattr(get_weather, "__tool_info__")
    """

    def decorator(func: Callable) -> Callable:
        schema = extract_function_schema(func, name, description)

        # Attach metadata
        func.__tool_info__ = FunctionToolInfo(  # type: ignore
            name=schema.name,
            description=schema.description,
            schema=schema,
            function=func,
        )

        return func

    # Handle both @function_tool and @function_tool()
    if callable(name):
        func = name
        name = None
        return decorator(func)

    return decorator


def is_function_tool(func: Any) -> bool:
    """
    Check if function is decorated with @function_tool.

    Args:
        func: Function to check

    Returns:
        True if decorated with @function_tool

    Example:
        @function_tool
        def my_tool(): pass

        assert is_function_tool(my_tool) == True
        assert is_function_tool(lambda: None) == False
    """
    return hasattr(func, "__tool_info__")


def find_function_tools(obj: Any) -> List[Callable]:
    """
    Discover all @function_tool decorated methods in an object.

    Useful for auto-registering all tools in a class.

    Args:
        obj: Object (class instance or class) to scan

    Returns:
        List of decorated functions

    Example:
        class MyAgent:
            @function_tool
            async def tool1(self, param: str):
                pass

            @function_tool
            async def tool2(self, param: int):
                pass

        agent = MyAgent()
        tools = find_function_tools(agent)
        assert len(tools) == 2
    """
    tools = []
    for name, member in inspect.getmembers(obj):
        if is_function_tool(member):
            tools.append(member)
    return tools
