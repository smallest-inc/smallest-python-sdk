"""Crew tool executions emit tool_call_start/end/error over the node's websocket,
so the platform surfaces them on the Events tab (parity with single-prompt agents).
"""

import asyncio

from smallestai.atoms.crew.clients.types import ToolCall
from smallestai.atoms.crew.events import SDKAgentLogEvent
from smallestai.atoms.crew.tools import ToolRegistry, function_tool


class _Node:
    """Minimal stand-in for a crew node: records events sent over the websocket."""

    def __init__(self):
        self.sent = []
        self.registry = ToolRegistry()
        self.registry.discover(self)

    async def send_event(self, event):
        self.sent.append(event)

    @function_tool(name="do_thing")
    async def do_thing(self, x: str) -> dict:
        return {"ok": True, "echo": x}

    @function_tool(name="boom")
    async def boom(self) -> None:
        raise RuntimeError("kaboom")


def _logs(node):
    return [e for e in node.sent if isinstance(e, SDKAgentLogEvent)]


def test_success_emits_start_and_end():
    node = _Node()
    call = ToolCall(id="c1", name="do_thing", arguments='{"x": "hi"}')
    asyncio.run(node.registry.execute([call], parallel=False))
    logs = _logs(node)
    names = [e.name for e in logs]
    assert names == ["tool_call_start", "tool_call_end"]
    start, end = logs
    assert start.payload["function_name"] == "do_thing"
    assert start.payload["tool_call_id"] == "c1"
    assert start.payload["context"]["arguments"] == {"x": "hi"}
    assert end.payload["success"] is True
    assert end.payload["context"]["response"] == {"ok": True, "echo": "hi"}
    assert "latency" in end.payload


def test_error_emits_start_and_error():
    node = _Node()
    call = ToolCall(id="c2", name="boom", arguments="{}")
    asyncio.run(node.registry.execute([call], parallel=False))
    names = [e.name for e in _logs(node)]
    assert names == ["tool_call_start", "tool_call_error"]
    err = _logs(node)[-1]
    assert err.payload["success"] is False
    assert "kaboom" in (err.payload.get("error") or "")


def test_standalone_registry_is_silent():
    # No owner node -> no events, no crash.
    reg = ToolRegistry()

    @function_tool(name="plain")
    async def plain(x: str) -> str:
        return x

    reg.register(plain)
    results = asyncio.run(reg.execute([ToolCall(id="c3", name="plain", arguments='{"x": "y"}')]))
    assert results[0].content


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
