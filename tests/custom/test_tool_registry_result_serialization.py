"""Regression test: a tool that succeeded is reported as succeeded.

`_execute_single` serialized dict/list results with a bare `json.dumps`, so a tool
returning e.g. `{"at": datetime(...)}` raised *after* the tool had run. The except
branch then emitted `tool_call_error` and handed the LLM `is_error=True` with
"Object of type datetime is not JSON serializable" — for a booking or payment tool,
an invitation to call it again and repeat the side effect.
"""

import asyncio
import datetime
import decimal
import json
import unittest
import uuid

from smallestai.atoms.crew.clients.types import ToolCall
from smallestai.atoms.crew.tools.decorator import function_tool
from smallestai.atoms.crew.tools.registry import ToolRegistry

_calls = []


@function_tool
async def book_slot(day: str) -> dict:
    """Book a slot.

    Args:
        day: day to book.
    """
    _calls.append(day)
    return {
        "booked": True,
        "at": datetime.datetime(2026, 9, 29, 10, 0),
        "price": decimal.Decimal("12.50"),
        "ref": uuid.UUID("12345678-1234-5678-1234-567812345678"),
    }


@function_tool
async def plain(x: str) -> dict:
    """A tool returning plain JSON.

    Args:
        x: anything.
    """
    return {"x": x, "n": [1, 2]}


class _Owner:
    def __init__(self):
        self.events = []

    async def send_event(self, event):
        self.events.append(event.name)


class ToolResultSerializationTest(unittest.TestCase):
    def setUp(self):
        _calls.clear()

    def test_non_json_values_in_result_are_not_a_tool_failure(self):
        registry = ToolRegistry()
        registry.register(book_slot)
        owner = _Owner()
        registry._owner = owner

        [result] = asyncio.run(registry.execute([ToolCall(id="c1", name="book_slot", arguments='{"day": "mon"}')]))

        self.assertEqual(_calls, ["mon"])
        self.assertFalse(result.is_error)
        self.assertEqual(result.tool_call_id, "c1")
        self.assertEqual(
            json.loads(result.content),
            {
                "booked": True,
                "at": "2026-09-29 10:00:00",
                "price": "12.50",
                "ref": "12345678-1234-5678-1234-567812345678",
            },
        )
        self.assertEqual(owner.events, ["tool_call_start", "tool_call_end"])

    def test_plain_json_result_is_unchanged(self):
        registry = ToolRegistry()
        registry.register(plain)

        [result] = asyncio.run(registry.execute([ToolCall(id="c2", name="plain", arguments='{"x": "a"}')]))

        self.assertFalse(result.is_error)
        self.assertEqual(result.content, json.dumps({"x": "a", "n": [1, 2]}))


if __name__ == "__main__":
    unittest.main()
