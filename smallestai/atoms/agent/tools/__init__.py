"""
Tool system for atoms-sdk.

Provides decorator-based tool registration and automatic execution.
"""

from smallestai.atoms.agent.tools.decorator import (
    find_function_tools,
    function_tool,
    is_function_tool,
)
from smallestai.atoms.agent.tools.registry import ToolRegistry
from smallestai.atoms.agent.tools.schema import FunctionSchema

__all__ = [
    "function_tool",
    "is_function_tool",
    "find_function_tools",
    "ToolRegistry",
    "FunctionSchema",
]
