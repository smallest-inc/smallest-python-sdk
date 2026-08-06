"""OutputCrewNode: framework routing must run even when a subclass overrides the
user hook without super(). Overriding `on_event` (the documented extension point)
must NOT silence the LLM-request -> generate_response path, and existing
`process_event`-with-super() overrides must keep working (backward compat)."""
import unittest
from unittest import mock

from smallestai.agents.crew.events import SDKSystemLLMRequestEvent
from smallestai.agents.crew.nodes import OutputCrewNode


class _OnEventAgent(OutputCrewNode):
    """Recommended pattern: override on_event, no super()."""
    def __init__(self, order):
        super().__init__(name="a")
        self._order = order

    async def on_event(self, event):
        self._order.append("on_event")

    async def generate_response(self):
        if False:
            yield ""


class _LegacyProcessEventAgent(OutputCrewNode):
    """Legacy pattern: override process_event and call super()."""
    def __init__(self, order):
        super().__init__(name="b")
        self._order = order

    async def process_event(self, event):
        await super().process_event(event)
        self._order.append("legacy_process_event")

    async def generate_response(self):
        if False:
            yield ""


class OnEventHookTest(unittest.IsolatedAsyncioTestCase):
    async def test_on_event_override_keeps_framework_routing(self):
        order = []
        a = _OnEventAgent(order)
        a._handle_llm_request = mock.AsyncMock(side_effect=lambda: order.append("llm"))
        a.send_event = mock.AsyncMock()
        await a.process_event(SDKSystemLLMRequestEvent())
        self.assertIn("llm", order, "framework LLM routing must run")
        self.assertIn("on_event", order, "user hook must run")
        self.assertLess(order.index("llm"), order.index("on_event"), "framework runs before user hook")

    async def test_legacy_process_event_with_super_still_routes(self):
        order = []
        b = _LegacyProcessEventAgent(order)
        b._handle_llm_request = mock.AsyncMock(side_effect=lambda: order.append("llm"))
        b.send_event = mock.AsyncMock()
        await b.process_event(SDKSystemLLMRequestEvent())
        self.assertIn("llm", order, "backward-compat: super() still routes")
        self.assertIn("legacy_process_event", order)


if __name__ == "__main__":
    unittest.main()
