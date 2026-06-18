import asyncio
import uuid
from typing import Awaitable, Callable, Dict, Optional

import uvicorn
from fastapi import FastAPI, WebSocket
from loguru import logger

from smallestai.atoms.crew.session import CrewSession


async def _dry_run_setup_handler(
    setup_handler: Callable[[CrewSession], Awaitable[None]],
) -> None:
    """Construct a no-op CrewSession and invoke the user's setup_handler.

    Used by `AtomsCrewApp._validate_startup` to surface any exception
    the setup_handler raises (typically when a node's `__init__` reads
    an env var that isn't set, or imports something that isn't
    installed) *before* the pod accepts a real WebSocket connection.

    Doesn't connect to any external services — node `start()` is never
    called. Only constructor / `add_node()` / `add_edge()` logic runs.
    """

    class _NullWebSocket:
        async def accept(self):
            return None

        async def send_bytes(self, data):
            return None

        async def receive_json(self, mode="binary"):
            await asyncio.sleep(3600)  # never returns
            return {}

        async def close(self, code=1000):
            return None

    session = CrewSession(
        websocket=_NullWebSocket(),  # type: ignore[arg-type]
        session_id="startup-validation",
        setup_handler=setup_handler,
    )
    # Don't `await session.initialize()` — that would actually wait on
    # the init handshake and start the receive loop. We only want to
    # exercise the user's setup_handler enough to surface __init__ errors.
    await setup_handler(session)


class SessionHandler:
    """Manages all active WebSocket sessions"""

    def __init__(self):
        self._sessions: Dict[str, CrewSession] = {}

    async def create_session(
        self,
        websocket: WebSocket,
        setup_handler: Callable[[CrewSession], Awaitable[None]],
    ) -> str:
        """
        Create and start a new session.

        Args:
            websocket: WebSocket connection
            session_id: Unique session ID
            setup_handler: Async function to setup the session graph
        """
        # Create session
        session_id = f"session-{uuid.uuid4()}"
        session = CrewSession(
            websocket=websocket, session_id=session_id, setup_handler=setup_handler
        )
        await session.initialize()

        self._sessions[session_id] = session

        return session_id

    def disconnect(self, session_id: str) -> None:
        """Remove a session"""
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.debug(f"Removed session {session_id}")

    @property
    def active_sessions(self) -> int:
        """Get number of active sessions"""
        return len(self._sessions)

    async def shutdown(self) -> None:
        """Shutdown all sessions"""
        if self._sessions:
            logger.info(f"Closing {len(self._sessions)} active sessions")
            await asyncio.gather(
                *[session.cleanup() for session in self._sessions.values()],
                return_exceptions=True,
            )

            self._sessions.clear()


class AtomsCrewApp:
    """
    FastAPI-based WebSocket server for Atoms SDK.

    Each incoming connection creates a new session with agent graph.

    Example:
        >>> from sdk.server import AtomsCrewApp
        >>> from sdk.nodes.base_node import CrewNode
        >>>
        >>> async def setup_session(session: CrewSession):
        ...     # Add nodes
        ...     node1 = MyNode()
        ...     session.add_node(node1)
        ...
        ...     # Add edges if multiple nodes
        ...     # session.add_edge(node1, node2)
        >>>
        >>> app = AtomsCrewApp(setup_handler=setup_session)
        >>> app.run(port=8080)
    """

    def __init__(
        self,
        setup_handler: Callable[[CrewSession], Awaitable[None]],
    ):
        """
        Initialize Atoms WebSocket server.

        Args:
            setup_handler: Async function to setup session graph
            host: Host to bind to
            port: Port to listen on
        """
        self._host = "0.0.0.0"
        self._port = 8080
        self.setup_handler = setup_handler

        # Readiness: pod accepts WebSocket sessions only after a dry-run
        # CrewSession construction has succeeded. Lets the orchestrator
        # / k8s readinessProbe catch broken builds (missing env vars,
        # bad imports, etc.) before any call is routed to this pod.
        self._ready: bool = False
        self._not_ready_reason: Optional[str] = None

        self.app = FastAPI(title="Atoms SDK Server", version="0.1.0")
        self.session_handler = SessionHandler()

        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup FastAPI routes"""

        @self.app.get("/")
        async def root():
            """Health check endpoint"""
            return {
                "status": "running",
                "ready": self._ready,
                "active_sessions": self.session_handler.active_sessions,
            }

        @self.app.get("/health")
        async def health():
            """Liveness probe — pod is alive."""
            return {
                "status": "ok",
                "active_sessions": self.session_handler.active_sessions,
            }

        @self.app.get("/ready")
        async def ready():
            """Readiness probe — pod is alive AND can accept new sessions.

            Returns 200 once `_validate_startup()` has succeeded.
            Returns 503 until then (or if startup failed).
            """
            if self._ready:
                return {
                    "status": "ready",
                    "active_sessions": self.session_handler.active_sessions,
                }
            from fastapi import HTTPException

            raise HTTPException(
                status_code=503,
                detail={
                    "status": "not_ready",
                    "reason": self._not_ready_reason or "startup not yet complete",
                },
            )

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """Main WebSocket endpoint for agent sessions"""

            session_id = None

            try:
                session_id = await self.session_handler.create_session(
                    websocket=websocket,
                    setup_handler=self.setup_handler,
                )
            finally:
                if session_id:
                    self.session_handler.disconnect(session_id=session_id)

        @self.app.on_event("startup")
        async def startup_event():
            """Run startup validation, then flip readiness to True.

            If validation raises, log and leave readiness=False so the
            orchestrator's readinessProbe never lets traffic in. The pod
            stays alive (HEALTHCHECK still passes via `/health`) so it
            can be inspected via `kubectl logs`.
            """
            await self._validate_startup()

        @self.app.on_event("shutdown")
        async def shutdown_event():
            """Cleanup on server shutdown"""
            logger.info("Server shutting down...")
            await self.session_handler.shutdown()

    async def _validate_startup(self) -> None:
        """Dry-run the setup_handler against a no-op session, catching
        any exceptions before traffic arrives.

        This catches:
        - Missing env vars referenced in node `__init__` (e.g. an
          OpenAIClient that fails when OPENAI_API_KEY is unset)
        - Import errors in user code
        - Type errors in node constructors

        If validation passes, the pod flips to ready. Otherwise it stays
        not-ready and the orchestrator's readinessProbe will fail the
        build promotion.
        """
        try:
            await _dry_run_setup_handler(self.setup_handler)
        except Exception as e:
            self._ready = False
            self._not_ready_reason = f"{type(e).__name__}: {e}"
            logger.error(
                f"Startup validation failed — pod will not accept sessions. "
                f"{type(e).__name__}: {e}"
            )
            logger.exception("Full traceback:")
            return

        self._ready = True
        logger.info("Startup validation passed — pod is ready.")

    def run(self, **kwargs) -> None:
        """
        Run the server (blocking).

        Args:
            **kwargs: Additional arguments to pass to uvicorn.run()
        """
        config = {
            "host": self._host,
            "port": self._port,
            "log_level": "info",
            **kwargs,
        }

        logger.info(f"Starting Atoms SDK server on ws://{self._host}:{self._port}/ws")
        uvicorn.run(self.app, **config)
