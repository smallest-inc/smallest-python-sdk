import asyncio
import uuid
from typing import Awaitable, Callable, Dict

import uvicorn
from fastapi import FastAPI, WebSocket
from loguru import logger

from smallestai.atoms.agent.session import AgentSession


class SessionHandler:
    """Manages all active WebSocket sessions"""

    def __init__(self):
        self._sessions: Dict[str, AgentSession] = {}

    async def create_session(
        self,
        websocket: WebSocket,
        setup_handler: Callable[[AgentSession], Awaitable[None]],
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
        session = AgentSession(
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


class AtomsApp:
    """
    FastAPI-based WebSocket server for Atoms SDK.

    Each incoming connection creates a new session with agent graph.

    Example:
        >>> from sdk.server import AtomsApp
        >>> from sdk.nodes.base_node import Node
        >>>
        >>> async def setup_session(session: AgentSession):
        ...     # Add nodes
        ...     node1 = MyNode()
        ...     session.add_node(node1)
        ...
        ...     # Add edges if multiple nodes
        ...     # session.add_edge(node1, node2)
        >>>
        >>> app = AtomsApp(setup_handler=setup_session)
        >>> app.run(port=8080)
    """

    def __init__(
        self,
        setup_handler: Callable[[AgentSession], Awaitable[None]],
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
                "active_sessions": self.session_handler.active_sessions,
            }

        @self.app.get("/health")
        async def health():
            """Health check endpoint"""
            return {
                "status": "ok",
                "active_sessions": self.session_handler.active_sessions,
            }

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

        @self.app.on_event("shutdown")
        async def shutdown_event():
            """Cleanup on server shutdown"""
            logger.info("Server shutting down...")
            await self.session_handler.shutdown()

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
