"""
Graph - Tree/DAG structure for agent nodes.

Supports building graphs from edges with validation:
- Multiple roots allowed
- No cycles
- Automatic sink connection for leaves
"""

import asyncio
import inspect
import json
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set, Tuple

from fastapi import WebSocket, WebSocketDisconnect
from loguru import logger
from pydantic import BaseModel

from smallestai.atoms.agent.events import (
    SDKAgentErrorEvent,
    SDKAgentReadyEvent,
    SDKEvent,
    SDKSystemInitEvent,
)
from smallestai.atoms.agent.nodes import Node
from smallestai.atoms.agent.task_manager import TaskManager, TaskManagerParams


@dataclass
class EventHandler:
    name: str
    handlers: List[Any]


class SessionConfig(BaseModel):
    """Configuration for the session"""

    edges: List[Tuple[Node, Node]] = []
    nodes: List[Node] = []
    name: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class EventCodec:
    def encode(self, data: SDKEvent) -> bytes:
        return json.dumps(
            {
                "type": data.type,
                **data.model_dump(mode="json"),
            }
        ).encode()

    def decode(self, data: Dict[str, Any]) -> SDKEvent:
        return SDKEvent.parse_obj(data)


class RootNode(Node):
    """
    Root node - entry point that receives events from WebSocket.
    """

    def __init__(self, name: str = "Root"):
        super().__init__(name=name)

    async def process_event(self, event: SDKEvent):
        await self.send_event(event)


class SinkNode(Node):
    """
    Sink node - exit point that sends events to WebSocket.

    All leaf nodes in the graph connect to this sink.
    """

    def __init__(self, session: "AgentSession", name: str = "Sink"):
        super().__init__(name=name)
        self._session = session

    async def process_event(self, event: SDKEvent):
        """Send event to WebSocket via session"""
        if self._session:
            await self._session.send_to_websocket(event)
        else:
            logger.warning(f"[{self.name}] No session available to send event")


class AgentSession:
    """
    Agent session that manages graph execution and WebSocket communication.

    Handles:
    - WebSocket connection lifecycle
    - Event routing from WebSocket to graph
    - Event routing from graph (sink) to WebSocket
    - Graph lifecycle management
    """

    def __init__(
        self,
        websocket: WebSocket,
        session_id: str,
        setup_handler: Callable[["AgentSession"], Awaitable[None]],
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        """
        Initialize the agent session.

        Args:
            websocket: FastAPI WebSocket connection
            session_id: Unique session identifier
        """
        self.name = f"Session-{session_id}"

        self.websocket = websocket
        self.session_id = session_id

        self._setup_handler = setup_handler

        self.nodes: List[Node] = []
        self.edges: List[Tuple[Node, Node]] = []

        self.root = RootNode(name=f"{self.name}::Root")
        self.sink = SinkNode(session=self, name=f"{self.name}::Sink")

        self.codec = EventCodec()
        self._running = False

        self._init_event: Optional[SDKSystemInitEvent] = None

        self.task_manager = TaskManager()

        self.loop = loop or asyncio.get_event_loop()

        self._receive_loop_task: Optional[asyncio.Task] = None

        self._shutdown_event = asyncio.Event()
        self._cleanup_complete = asyncio.Event()

        self._event_tasks: Set[asyncio.Task] = set()
        self._event_handlers: Dict[str, EventHandler] = {}

        self._register_event_handler("on_event_received")

    async def initialize(self):
        """Initialize the session"""
        logger.info(f"[{self.name}] Initializing session")

        self.task_manager.setup(TaskManagerParams(loop=self.loop))

        await self.websocket.accept()

        await self._handle_init_event()

        await self._setup_handler(self)

    async def _handle_init_event(self) -> None:
        """
        Handle the handshake protocol.

        Returns:
            bool: True if handshake successful, False otherwise
        """
        try:
            message = await asyncio.wait_for(
                self.websocket.receive_json(mode="binary"), timeout=10.0
            )
            logger.info(f"Received message: {message}")

            init_event = self.codec.decode(message)
            logger.info(f"Received handshake event: {init_event}")

            if not isinstance(init_event, SDKSystemInitEvent):
                logger.error(f"Expected HandshakeEvent, got {type(init_event)}")
                error_event = SDKAgentErrorEvent(
                    message=f"Expected InitEvent, got {type(init_event)}"
                )
                await self.send_to_websocket(error_event)
                # TODO: End the pipeline means disconnect the websocket because we have to not called the run handler

            if isinstance(init_event, SDKSystemInitEvent):
                self._init_event = init_event
                logger.info(
                    f"Received handshake: version={init_event.version}, "
                    f"conversation_type={init_event.session_context.conversation_type}"
                )

        except asyncio.TimeoutError:
            logger.error("Init timeout")
            # TODO: End the pipeline means disconnect the websocket because we have to not called the run handler

        except Exception as e:
            logger.error(f"Init error: {e}")
            # TODO: End the pipeline means disconnect the websocket because we have to not called the run handler

    def add_node(self, node: Node):
        """Add a node to the session graph"""
        self.nodes.append(node)
        logger.debug(f"[{self.name}] Added node: {node.name}")

    def add_edge(self, parent: Node, child: Node):
        """Add an edge between nodes"""
        self.edges.append((parent, child))
        logger.debug(f"[{self.name}] Added edge: {parent.name} -> {child.name}")

    async def start(self) -> None:
        """Start the session"""
        logger.info(f"[{self.name}] Starting session")
        if not self._init_event:
            logger.error(
                "This should not happen because this method should always be called after the init event is received which will set the init event"
            )
            raise ValueError("Session not initialized")

        logger.info(f"[{self.name}] Building graph with {len(self.nodes)} nodes")
        self._build_graph()

        self._running = True

        await self._start_nodes(self._init_event, self.task_manager)
        await self.send_to_websocket(SDKAgentReadyEvent())

        self._receive_loop_task = self.task_manager.create_task(
            self._receive_loop(), name="receive_loop"
        )

    def _build_graph(self):
        """Build and validate the graph"""
        for parent, child in self.edges:
            parent.add_child(child)

        nodes_with_no_parents = [node for node in self.nodes if not node.has_parents]
        for node in nodes_with_no_parents:
            self.root.add_child(node)

        nodes_with_no_children = [node for node in self.nodes if not node.has_children]

        for node in nodes_with_no_children:
            self.sink.add_parent(node)

        self.nodes = [self.root] + self.nodes + [self.sink]

        logger.info(f"[{self.name}] Graph built: {len(self.nodes)} nodes, ")

        if self._has_cycle():
            raise ValueError(f"[{self.name}] Graph contains cycles!")

    def _has_cycle(self) -> bool:
        """Detect if graph has cycles using DFS with colors"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in self.nodes}

        def dfs(node: Node) -> bool:
            if color[node] == GRAY:
                return True
            if color[node] == BLACK:
                return False

            color[node] = GRAY

            for child in node.children:
                if child in color and dfs(child):
                    return True

            color[node] = BLACK
            return False

        if dfs(self.root):
            return True

        return False

    async def _start_nodes(
        self, init_event: SDKSystemInitEvent, task_manager: TaskManager
    ):
        """Start all nodes including sink"""
        for node in self.nodes:
            await node.start(init_event, task_manager)
        logger.info(f"[{self.name}] All nodes started")

    async def _receive_loop(self):
        """Receive and process messages from WebSocket"""
        try:
            while self._running:
                data = await self.websocket.receive_json(mode="binary")
                try:
                    event = self.codec.decode(data)
                    await self.root.queue_event(event)

                    await self._call_event_handler("on_event_received", event)

                except Exception as e:
                    logger.error(f"Error in receive loop: {e}", exc_info=True)
        except WebSocketDisconnect:
            logger.info(f"[{self.name}] WebSocket disconnected in receive loop")
            await self.cleanup()
        except Exception as e:
            logger.error(f"[{self.name}] Error in receive loop: {e}", exc_info=True)
            await self.cleanup()

    async def send_to_websocket(self, event: SDKEvent):
        """Send event to WebSocket (called by sink)"""
        try:
            encoded_event = self.codec.encode(event)
            await self.websocket.send_bytes(encoded_event)
            logger.trace(f"[{self.name}] Sent to WebSocket: {event.type}")
        except Exception as e:
            logger.error(f"[{self.name}] Failed to send to WebSocket: {e}")

    async def stop(self):
        """Stop the session"""
        for node in self.nodes:
            await node.stop()

    async def cleanup(self):
        """Cleanup session resources"""
        if not self._running:
            return

        logger.info(f"[{self.name}] Starting cleanup")
        self._running = False

        for task in self._event_tasks:
            if self.task_manager:
                await self.task_manager.cancel_task(task)
        self._event_tasks.clear()

        await self.stop()

        try:
            await self.websocket.close()
            logger.debug(f"[{self.name}] WebSocket closed in cleanup")
        except Exception:
            logger.debug("Websocket already closed in cleanup")

        if self._receive_loop_task:
            await self.task_manager.cancel_task(self._receive_loop_task)
            self._receive_loop_task = None

        current_tasks = self.task_manager.current_tasks()
        if current_tasks:
            task_names = ", ".join(list(self.task_manager._tasks.keys()))
            logger.info(f"[{self.name}] Tasks: {task_names}")
            logger.info(
                f"[{self.name}] Waiting for {len(current_tasks)} tasks to complete"
            )
            await asyncio.gather(*current_tasks, return_exceptions=True)

        self._cleanup_complete.set()
        logger.info(f"[{self.name}] Cleanup complete")

    async def wait_until_complete(self):
        """Wait until the session is complete and cleaned up."""
        await self._cleanup_complete.wait()
        logger.info(f"[{self.name}] Session complete")

    def on_event(self, event_name: str):
        """Decorator for registering event handlers.
        Args:
            event_name: The name of the event to handle.
        Returns:
            The decorator function that registers the handler.
        """

        def decorator(handler):
            self.add_event_handler(event_name, handler)
            return handler

        return decorator

    def add_event_handler(self, event_name: str, handler):
        """Add an event handler for the specified event.
        Args:
            event_name: The name of the event to handle.
            handler: The function to call when the event occurs.
                Can be sync or async.
        """
        if event_name in self._event_handlers:
            self._event_handlers[event_name].handlers.append(handler)
        else:
            logger.warning(f"Event handler {event_name} not registered")

    def _register_event_handler(self, event_name: str):
        """Register an event handler type.
        Args:
            event_name: The name of the event type to register.
            sync: Whether this event handler will be executed in a task.
        """
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = EventHandler(
                name=event_name, handlers=[]
            )
        else:
            logger.warning(f"Event handler {event_name} already registered")

    async def _run_handler(self, event_name: str, handler, *args, **kwargs):
        """Execute all handlers for an event.
        Args:
            event_name: The event name for this handler.
            handler: The handler function to run.
            *args: Positional arguments to pass to handlers.
            **kwargs: Keyword arguments to pass to handlers.
        """
        try:
            if inspect.iscoroutinefunction(handler):
                await handler(self, *args, **kwargs)
            else:
                handler(self, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Exception in event handler {event_name}: {e}")

    async def _call_event_handler(self, event_name: str, *args, **kwargs):
        """Call all registered handlers for the specified event.
        Args:
            event_name: The name of the event to trigger.
            *args: Positional arguments to pass to event handlers.
            **kwargs: Keyword arguments to pass to event handlers.
        """
        if event_name not in self._event_handlers:
            logger.warning(f"Event handler {event_name} not registered")
            return

        event_handler = self._event_handlers[event_name]

        for handler in event_handler.handlers:
            if self.task_manager:
                task_name = f"{self.name}::{event_name}::{handler.__name__}::handler"
                task = self.task_manager.create_task(
                    self._run_handler(event_name, handler, *args, **kwargs),
                    name=task_name,
                )
                self._event_tasks.add(task)

    def __repr__(self):
        return f"<AgentSession: {self.name} ({len(self.nodes)} nodes)>"
