"""Regression test: a parallel tool failure keeps the id the LLM needs.

`_execute_single` swallows every `Exception` and returns a `ToolResult` carrying the
call's id, so the fallback in `_execute_parallel` only ever sees a `BaseException`.
That fallback built its result with `tool_call_id=""` and `name=""`, which reaches the
model as `{"role": "tool", "tool_call_id": "", ...}`. A tool message has to name the
call it answers, so the whole request is malformed rather than merely uninformative.

`asyncio.CancelledError` is the `BaseException` that actually turns up here, and
turning it into a result let a cancelled turn carry on.
"""

import asyncio
import json
import unittest

from smallestai.atoms.crew.clients.types import ToolCall
from smallestai.atoms.crew.tools.decorator import function_tool
from smallestai.atoms.crew.tools.registry import ToolRegistry


class _Fatal(BaseException):
    """A BaseException that is not cancellation, so it still becomes a tool result."""


@function_tool
async def works(x: str) -> str:
    """A tool that succeeds.

    Args:
        x: anything.
    """
    return "ok"


@function_tool
async def fatal(x: str) -> str:
    """A tool that raises a BaseException.

    Args:
        x: anything.
    """
    raise _Fatal("boom")


@function_tool
async def silent(x: str) -> str:
    """A tool whose BaseException carries no message, so str() on it is empty.

    Args:
        x: anything.
    """
    raise _Fatal()


@function_tool
async def cancels(x: str) -> str:
    """A tool that is cancelled.

    Args:
        x: anything.
    """
    raise asyncio.CancelledError()


@function_tool
async def explodes(x: str) -> str:
    """A tool that raises an ordinary Exception.

    Args:
        x: anything.
    """
    raise ValueError("ordinary failure")


def _call(call_id: str, name: str) -> ToolCall:
    return ToolCall(id=call_id, name=name, arguments=json.dumps({"x": "1"}))


class ParallelToolErrorTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.registry = ToolRegistry()
        for tool in (works, fatal, silent, cancels, explodes):
            self.registry.register(tool)

    async def test_a_base_exception_result_keeps_its_call_id_and_name(self):
        results = await self.registry.execute([_call("call_bbb", "fatal")], parallel=True)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].tool_call_id, "call_bbb")
        self.assertEqual(results[0].name, "fatal")
        self.assertTrue(results[0].is_error)

    async def test_the_error_message_is_never_blank(self):
        """str() on a message-less exception is empty, which left the model a tool
        message with no content at all. Fall back to the exception's type name."""
        results = await self.registry.execute([_call("call_ccc", "silent")], parallel=True)

        self.assertTrue(results[0].content)
        self.assertIn("_Fatal", results[0].content)

    async def test_results_stay_aligned_with_their_calls(self):
        calls = [
            _call("call_1", "works"),
            _call("call_2", "fatal"),
            _call("call_3", "works"),
        ]

        results = await self.registry.execute(calls, parallel=True)

        self.assertEqual([r.tool_call_id for r in results], ["call_1", "call_2", "call_3"])
        self.assertEqual([r.is_error for r in results], [False, True, False])

    async def test_cancellation_propagates_instead_of_becoming_a_result(self):
        calls = [_call("call_1", "works"), _call("call_2", "cancels")]

        with self.assertRaises(asyncio.CancelledError):
            await self.registry.execute(calls, parallel=True)

    async def test_an_ordinary_exception_is_still_reported_as_a_tool_result(self):
        """That path never reaches the fallback; it must keep working unchanged."""
        results = await self.registry.execute([_call("call_ddd", "explodes")], parallel=True)

        self.assertEqual(results[0].tool_call_id, "call_ddd")
        self.assertEqual(results[0].name, "explodes")
        self.assertTrue(results[0].is_error)
        self.assertIn("ordinary failure", results[0].content)

    async def test_sequential_execution_is_unchanged(self):
        results = await self.registry.execute([_call("call_eee", "explodes")], parallel=False)

        self.assertEqual(results[0].tool_call_id, "call_eee")
        self.assertTrue(results[0].is_error)


if __name__ == "__main__":
    unittest.main()
