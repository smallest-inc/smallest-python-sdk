"""
CrewNode - Base class for graph-based agent nodes.

Supports tree/graph structures with multiple children and parents.
"""

import asyncio
import traceback as _traceback
from typing import Optional, Set

from loguru import logger

from smallestai.atoms.crew.events import (
    SDKAgentErrorEvent,
    SDKEvent,
    SDKSystemControlInterruptEvent,
    SDKSystemInitEvent,
)
from smallestai.atoms.crew.task_manager import TaskManager


class CrewNode:
    """Base class for nodes in the graph.

    Nodes are the building blocks of the graph. They can be linked together to form a tree or DAG.
    Each node can have multiple children and parents (for graph structures).

    Nodes can be of different types:
    - Root: nodes that receive events from outside (no parents)
    - Processor: nodes that process events (have parents and children)
    - Leaf: nodes at the end of branches (no children, connect to sink)
    - Sink: special node that outputs to WebSocket
    """

    def __init__(self, name: Optional[str] = None, is_interruptible: bool = False):
        """
        Initialize the node.

        Args:
            name: Optional name for this node
        """
        self.name = name or self.__class__.__name__

        # Graph structure - support multiple parents and children
        self._parents: Set["CrewNode"] = set()
        self._children: Set["CrewNode"] = set()

        # Event queue for this node
        self._queue: asyncio.Queue = asyncio.Queue()

        # Task management
        self._running = False

        self._task_manager: Optional[TaskManager] = None

        self._process_event_task: Optional[asyncio.Task] = None

        self._is_interruptible = is_interruptible

    @property
    def is_interruptible(self) -> bool:
        """Get whether this node is interruptible"""
        return self._is_interruptible

    @property
    def task_manager(self) -> Optional[TaskManager]:
        """Get the task manager for this node"""
        if not self._running:
            return None
        if not self._task_manager:
            raise ValueError(f"Task manager not set for node {self.name}")
        return self._task_manager

    def add_child(self, child: "CrewNode"):
        """Add a child node"""
        self._children.add(child)
        child._parents.add(self)
        logger.debug(f"Linked {self.name} -> {child.name}")

    def add_parent(self, parent: "CrewNode"):
        """Add a parent node"""
        self._parents.add(parent)
        parent._children.add(self)
        logger.debug(f"Linked {parent.name} -> {self.name}")

    @property
    def children(self) -> Set["CrewNode"]:
        """Get all child nodes"""
        return self._children

    @property
    def parents(self) -> Set["CrewNode"]:
        """Get all parent nodes"""
        return self._parents

    @property
    def has_parents(self) -> bool:
        """Check if this node has parents"""
        return len(self._parents) > 0

    @property
    def has_children(self) -> bool:
        """Check if this node has children"""
        return len(self._children) > 0

    async def queue_event(self, event: SDKEvent):
        """
        Queue an event for processing by this node.

        Args:
            event: The event to queue
        """
        await self._queue.put(event)

    async def send_event(self, event: SDKEvent):
        """
        Send an event in the specified direction.

        Args:
            event: The event to send
            direction: The direction to send the event
        """
        for child in self._children:
            logger.trace(f"[{self.name}] Sending event to {child.name}")
            if isinstance(event, SDKSystemControlInterruptEvent):
                await child.process_event(event)
            else:
                await child.queue_event(event)

    async def _handle_interrupt(self):
        """Handle interrupt"""

        await self.__cancel_process_event_task()
        self._queue = asyncio.Queue()
        await self.__create_process_event_task()

    async def process_event(self, event: SDKEvent):
        """
        Process an event (override this in subclass).

        Args:
            event: The event to process
        """

        if isinstance(event, SDKSystemControlInterruptEvent) and self.is_interruptible:
            await self._handle_interrupt()

    async def __process_event_handler_loop(self):
        """Process event handler loop.

        Each `process_event` call is wrapped in try/except so a single user-code
        exception doesn't kill the node's event loop (previously: one exception
        would tear down the whole loop and silently stop processing future
        events). On error, an `SDKAgentErrorEvent` is emitted upstream so the
        orchestrator can record it on the call's `errors[]` and surface it in
        the Events tab. Severity is determined by node type:

        - `BackgroundCrewNode` subclasses → `severity="warning"` (call continues)
        - All other node types (output, custom) → `severity="fatal"` (call fails)
        """
        while self._running:
            try:
                event = await self._queue.get()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception(f"[{self.name}] Error reading from event queue")
                continue

            if event is None:
                break

            try:
                await self.process_event(event)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                severity = self._error_severity()
                tb_str = _traceback.format_exc()
                logger.error(
                    f"[{self.name}] {severity.upper()} in process_event: "
                    f"{type(e).__name__}: {e}\n{tb_str}"
                )
                try:
                    await self.send_event(SDKAgentErrorEvent(
                        message=f"{type(e).__name__} in {self.name}.process_event: {e}",
                        severity=severity,
                        payload={
                            "node_name": self.name,
                            "error_class": type(e).__name__,
                            "traceback": tb_str,
                        },
                    ))
                except Exception:
                    logger.exception(
                        f"[{self.name}] Failed to emit SDKAgentErrorEvent upstream"
                    )

    def _error_severity(self) -> str:
        """Return the default error severity for this node type.

        Subclasses can override to change classification. Output-style nodes
        (the user-facing agent) are fatal; observation-style nodes
        (`BackgroundCrewNode`) are warnings.
        """
        # Local import avoids a circular dep at module-load time.
        from smallestai.atoms.crew.nodes.background_crew import BackgroundCrewNode
        return "warning" if isinstance(self, BackgroundCrewNode) else "fatal"

    async def __create_process_event_task(self):
        """Create a task to process events"""
        if self.task_manager:
            self._process_event_task = self.task_manager.create_task(
                self.__process_event_handler_loop(),
                name=f"{self.name}::process_event_handler_loop",
            )

    async def __cancel_process_event_task(self):
        """Cancel the task to process events"""
        if self.task_manager and self._process_event_task:
            await self.task_manager.cancel_task(self._process_event_task)
            self._process_event_task = None

    async def start(self, init_event: SDKSystemInitEvent, task_manager: TaskManager):
        """Start the node"""
        if self._running:
            logger.warning(f"[{self.name}] Already running")
            return

        self._running = True
        self._task_manager = task_manager
        await self.__create_process_event_task()
        logger.info(f"[{self.name}] Started")

    async def stop(self):
        """Stop the agent processor"""
        if not self._running:
            return

        self._running = False
        await self._queue.put(None)

        await self.__cancel_process_event_task()
        logger.info(f"[{self.name}] Stopped")

    def __repr__(self):
        return f"<CrewNode: {self.name}>"
