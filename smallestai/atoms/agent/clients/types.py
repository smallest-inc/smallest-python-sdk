"""
Type definitions for LLM clients.

Common types used across different LLM providers.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ToolCall:
    """Function/tool call from LLM."""

    id: str
    name: str
    arguments: str  # JSON string

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "id": self.id,
            "type": "function",
            "function": {"name": self.name, "arguments": self.arguments},
        }


@dataclass
class ChatChunk:
    """Single chunk from streaming response."""

    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    finish_reason: Optional[str] = None


@dataclass
class ChatResponse:
    """Complete non-streaming response."""

    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    usage: Optional[Dict[str, Any]] = None


@dataclass
class ToolResult:
    """Result from tool execution."""

    tool_call_id: str
    name: str
    content: str
    is_error: bool = False

    def to_message(self) -> Dict[str, Any]:
        """Convert to OpenAI message format."""
        return {
            "role": "tool",
            "tool_call_id": self.tool_call_id,
            "name": self.name,
            "content": self.content,
        }
