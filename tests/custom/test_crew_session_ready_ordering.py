"""Regression test: CrewSession.start() must send SDKAgentReadyEvent BEFORE
starting nodes, so a node's start() that emits a speak (e.g. a greeting) doesn't
reach the platform before Ready and poison the connect handshake."""

import unittest
from unittest import mock

from smallestai.atoms.crew.nodes import OutputCrewNode
from smallestai.atoms.crew.session import CrewSession


class _OrderNode(OutputCrewNode):
    def __init__(self, order):
        super().__init__(name="rec")
        self._order = order

    async def start(self, init_event, task_manager):
        await super().start(init_event, task_manager)
        self._order.append("node_started")

    async def generate_response(self):
        if False:
            yield ""  # never runs; satisfies the abstract async-generator


class ReadyBeforeNodesTest(unittest.IsolatedAsyncioTestCase):
    async def test_ready_sent_before_nodes_start(self):
        order = []
        session = CrewSession(websocket=mock.AsyncMock(), session_id="t", setup_handler=None)
        session._init_event = mock.MagicMock()
        session.task_manager = mock.MagicMock()
        session.task_manager.create_task = mock.MagicMock()  # don't run receive loop
        session._receive_loop = mock.MagicMock()  # avoid unawaited-coroutine warning

        async def _record_ready(event):
            order.append("ready_sent")

        session.send_to_websocket = _record_ready
        session.add_node(_OrderNode(order))

        await session.start()

        self.assertIn("ready_sent", order)
        self.assertIn("node_started", order)
        self.assertLess(
            order.index("ready_sent"),
            order.index("node_started"),
            f"Ready must be sent before nodes start; got order={order}",
        )


if __name__ == "__main__":
    unittest.main()
