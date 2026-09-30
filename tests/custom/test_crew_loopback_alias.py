"""@loopback_tool is the Line-parity alias of @function_tool (result -> LLM, the default)."""

import unittest

from smallestai.atoms.crew import function_tool, loopback_tool
from smallestai.atoms.crew.tools.decorator import is_function_tool


class LoopbackAliasTest(unittest.TestCase):
    def test_loopback_tool_is_function_tool(self):
        self.assertIs(loopback_tool, function_tool)

    def test_loopback_decorated_is_a_registered_tool(self):
        @loopback_tool
        async def get_order_status(order_id: str) -> str:
            """Look up an order.

            Args:
                order_id: the order id.
            """
            return "ok"

        self.assertTrue(is_function_tool(get_order_status))
        self.assertTrue(hasattr(get_order_status, "__tool_info__"))


if __name__ == "__main__":
    unittest.main()
