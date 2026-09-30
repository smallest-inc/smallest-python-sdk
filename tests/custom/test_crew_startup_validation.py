"""Startup validation dry-run.

A healthy `setup_handler` that ends with `await session.start()` (the canonical
pattern) must pass validation without logging an error. Only handlers that raise
during node construction / graph build (missing env, bad import, cycles) should
fail validation and leave the pod not-ready.
"""

import unittest

from smallestai.atoms.crew.nodes import OutputCrewNode
from smallestai.atoms.crew.server import AtomsCrewApp, _dry_run_setup_handler
from smallestai.atoms.crew.session import CrewSession, _StartupProbeComplete


class _Assistant(OutputCrewNode):
    def __init__(self):
        super().__init__(name="assistant")

    async def generate_response(self):
        if False:
            yield ""  # never runs; satisfies the abstract async-generator


class StartupValidationTest(unittest.IsolatedAsyncioTestCase):
    async def test_canonical_handler_passes_validation(self):
        # Canonical handler: build a node, then `await session.start()`.
        async def setup(session: CrewSession):
            session.add_node(_Assistant())
            await session.start()
            # Real handlers continue here (event handlers, wait_until_complete);
            # the dry-run halts at start(), so this is never reached.
            raise AssertionError("dry-run should have halted at start()")

        # Should NOT raise: start() raises _StartupProbeComplete internally,
        # which _dry_run_setup_handler swallows.
        await _dry_run_setup_handler(setup)

        app = AtomsCrewApp(setup_handler=setup)
        await app._validate_startup()
        self.assertTrue(app._ready)
        self.assertIsNone(app._not_ready_reason)

    async def test_broken_handler_fails_validation(self):
        # A node whose __init__ raises (e.g. missing env var) must fail.
        class _Broken(OutputCrewNode):
            def __init__(self):
                super().__init__(name="broken")
                raise ValueError("MISSING_API_KEY not set")

            async def generate_response(self):
                if False:
                    yield ""

        async def setup(session: CrewSession):
            session.add_node(_Broken())
            await session.start()

        app = AtomsCrewApp(setup_handler=setup)
        await app._validate_startup()
        self.assertFalse(app._ready)
        self.assertIn("MISSING_API_KEY", app._not_ready_reason or "")

    async def test_dry_run_start_raises_probe_complete_and_builds_graph(self):
        session = CrewSession(websocket=None, session_id="t", setup_handler=None)  # type: ignore[arg-type]
        session._dry_run = True
        session.add_node(_Assistant())
        with self.assertRaises(_StartupProbeComplete):
            await session.start()
        # graph was built (root + node + sink), and no init event was required
        self.assertGreaterEqual(len(session.nodes), 3)
        self.assertIsNone(session._init_event)


if __name__ == "__main__":
    unittest.main()
