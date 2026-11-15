"""Regression test: a no-argument tool call with empty arguments still runs.

`OpenAIClient` accumulates streamed argument deltas starting from "" and skips
empty ones, so a call to a zero-parameter tool (end_call, transfer, ...) from a
provider that streams no argument text arrives with `arguments == ""`.
`json.loads("")` raised, so the tool never ran and the LLM got
"Expecting value: line 1 column 1 (char 0)" back as an error.
"""

import asyncio
import unittest

from smallestai.atoms.crew.clients.types import ToolCall
from smallestai.atoms.crew.tools.decorator import function_tool
from smallestai.atoms.crew.tools.registry import ToolRegistry

_calls = []


@function_tool
async def end_call() -> str:
    """End the call."""
    _calls.append("end_call")
    return "ended"


@function_tool
async def needs_arg(x: str) -> str:
    """A tool with a parameter.

    Args:
        x: anything.
    """
    return x


class EmptyArgumentsTest(unittest.TestCase):
    def setUp(self):
        _calls.clear()

    def _run(self, name, arguments):
        registry = ToolRegistry()
        registry.register(end_call)
        registry.register(needs_arg)
        [result] = asyncio.run(registry.execute([ToolCall(id="c1", name=name, arguments=arguments)]))
        return result

    def test_empty_and_blank_arguments_mean_no_arguments(self):
        for arguments in ("", "  ", "{}"):
            with self.subTest(arguments=arguments):
                _calls.clear()
                result = self._run("end_call", arguments)
                self.assertFalse(result.is_error, result.content)
                self.assertEqual(result.content, '"ended"')
                self.assertEqual(_calls, ["end_call"])

    def test_malformed_arguments_are_still_an_error(self):
        result = self._run("needs_arg", "{not json")
        self.assertTrue(result.is_error)
        self.assertEqual(result.tool_call_id, "c1")


if __name__ == "__main__":
    unittest.main()
