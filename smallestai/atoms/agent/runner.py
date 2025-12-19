# """
# Graph Runner - Manages graph execution with lifecycle and signal handling.

# Provides high-level interface for running graphs with automatic signal handling,
# graceful shutdown, and resource cleanup.
# """

# import asyncio
# import gc
# import signal
# from typing import Optional

# from loguru import logger

# from sdk.session import AgentSession


# class GraphRunner:
#     """
#     Manages the execution of graphs with lifecycle and signal handling.

#     Features:
#     - Automatic SIGINT/SIGTERM handling
#     - Graceful shutdown
#     - Timeout support
#     - Resource cleanup
#     - Optional garbage collection

#     Example:
#         >>> runner = GraphRunner(handle_sigint=True)
#         >>> graph = Graph(config=config)
#         >>> await runner.run(graph)
#     """

#     def __init__(
#         self,
#         name: Optional[str] = None,
#         handle_sigint: bool = True,
#         handle_sigterm: bool = False,
#         timeout: Optional[float] = None,
#         force_gc: bool = False,
#         loop: Optional[asyncio.AbstractEventLoop] = None,
#     ):
#         """
#         Initialize the graph runner.

#         Args:
#             name: Optional name for the runner instance
#             handle_sigint: Whether to handle SIGINT (Ctrl+C) signals
#             handle_sigterm: Whether to handle SIGTERM signals
#             timeout: Optional timeout in seconds for graph execution
#             force_gc: Whether to force garbage collection after completion
#             loop: Event loop to use (defaults to current running loop)
#         """
#         self.name = name or f"GraphRunner-{id(self)}"
#         self._sig_task: Optional[asyncio.Task] = None
#         self._force_gc = force_gc
#         self._timeout = timeout
#         self._loop = loop
#         self._running = False

#         # Setup signal handlers
#         if handle_sigint:
#             self._setup_sigint()

#         if handle_sigterm:
#             self._setup_sigterm()

#     async def run(self, session: AgentSession):
#         """
#         Run a session to completion.

#         Args:
#             session: The agent session to execute
#         """
#         logger.info(f"[{self.name}] Starting session: {session.name}")

#         self._running = True

#         try:
#             # Start the session
#             await session.start()

#             # Wait for completion with optional timeout
#             if self._timeout:
#                 try:
#                     await asyncio.wait_for(self._wait_for_session(session), timeout=self._timeout)
#                 except asyncio.TimeoutError:
#                     logger.warning(
#                         f"[{self.name}] Session {session.name} timed out after {self._timeout} seconds"
#                     )
#                     await self.cancel()
#             else:
#                 await self._wait_for_session(session)

#         finally:
#             # Cleanup
#             await self._cleanup_session(session)

#             # Wait for signal task if present
#             if self._sig_task:
#                 try:
#                     await self._sig_task
#                 except asyncio.CancelledError:
#                     pass

#             # Force garbage collection if requested
#             if self._force_gc:
#                 self._gc_collect()

#             logger.info(f"[{self.name}] Finished running session: {session.name}")

#     async def _wait_for_session(self, session: AgentSession):
#         """
#         Wait for session to complete.

#         For now, this just sleeps forever since sessions run continuously
#         until cancelled. Override this if you need custom completion logic.
#         """
#         try:
#             while self._running:
#                 await asyncio.sleep(1)
#         except asyncio.CancelledError:
#             logger.debug(f"[{self.name}] Session wait cancelled")
#             raise

#     async def stop_when_done(self):
#         """
#         Schedule all running sessions to stop gracefully.

#         This will stop accepting new events and wait for current
#         processing to complete.
#         """
#         logger.info(f"[{self.name}] Scheduling graceful stop")
#         self._running = False

#     async def cancel(self):
#         """Cancel all running sessions immediately."""
#         logger.warning(f"[{self.name}] Cancelling all sessions")
#         await self._cancel_all()

#     async def _cancel_all(self):
#         """Cancel all running sessions."""
#         self._running = False

#     async def _cleanup_session(self, session: AgentSession):
#         """Cleanup a specific session."""
#         try:
#             await session.stop()
#         except Exception as e:
#             logger.error(f"[{self.name}] Error stopping session {session.name}: {e}")

#     def _setup_sigint(self):
#         """Set up SIGINT (Ctrl+C) signal handler."""
#         try:
#             loop = self._loop or asyncio.get_running_loop()
#             loop.add_signal_handler(signal.SIGINT, lambda: self._sig_handler("SIGINT"))
#             logger.debug(f"[{self.name}] SIGINT handler registered")
#         except NotImplementedError:
#             # Windows fallback
#             signal.signal(signal.SIGINT, lambda s, f: self._sig_handler("SIGINT"))
#             logger.debug(f"[{self.name}] SIGINT handler registered (Windows mode)")

#     def _setup_sigterm(self):
#         """Set up SIGTERM signal handler."""
#         try:
#             loop = self._loop or asyncio.get_running_loop()
#             loop.add_signal_handler(signal.SIGTERM, lambda: self._sig_handler("SIGTERM"))
#             logger.debug(f"[{self.name}] SIGTERM handler registered")
#         except NotImplementedError:
#             # Windows fallback
#             signal.signal(signal.SIGTERM, lambda s, f: self._sig_handler("SIGTERM"))
#             logger.debug(f"[{self.name}] SIGTERM handler registered (Windows mode)")

#     def _sig_handler(self, signal_name: str = "SIGNAL"):
#         """
#         Handle interrupt signals.

#         Args:
#             signal_name: Name of the signal received
#         """
#         if not self._sig_task:
#             logger.warning(f"[{self.name}] {signal_name} received, initiating graceful shutdown")
#             self._sig_task = asyncio.create_task(self._sig_cancel())

#     async def _sig_cancel(self):
#         """Cancel all running graphs due to signal interruption."""
#         await self.cancel()

#     def _gc_collect(self):
#         """Force garbage collection and log results."""
#         collected = gc.collect()
#         logger.debug(f"[{self.name}] Garbage collected {collected} objects")

#         if gc.garbage:
#             logger.warning(f"[{self.name}] Found {len(gc.garbage)} uncollectable objects")

#     def __repr__(self):
#         return f"<GraphRunner: {self.name}>"
