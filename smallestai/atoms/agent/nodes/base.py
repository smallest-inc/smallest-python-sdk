"""
Node - Base class for graph-based agent nodes.

Supports tree/graph structures with multiple children and parents.
"""

import asyncio
from typing import Optional, Set

from loguru import logger

from smallestai.atoms.agent.events import (
    SDKEvent,
    SDKSystemControlInterruptEvent,
    SDKSystemInitEvent,
)
from smallestai.atoms.agent.task_manager import TaskManager


class Node:
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
        self._parents: Set["Node"] = set()
        self._children: Set["Node"] = set()

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

    def add_child(self, child: "Node"):
        """Add a child node"""
        self._children.add(child)
        child._parents.add(self)
        logger.debug(f"Linked {self.name} -> {child.name}")

    def add_parent(self, parent: "Node"):
        """Add a parent node"""
        self._parents.add(parent)
        parent._children.add(self)
        logger.debug(f"Linked {parent.name} -> {self.name}")

    @property
    def children(self) -> Set["Node"]:
        """Get all child nodes"""
        return self._children

    @property
    def parents(self) -> Set["Node"]:
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
        """Process event handler loop"""
        try:
            while self._running:
                event = await self._queue.get()

                if event is None:
                    break

                await self.process_event(event)
        except Exception as e:
            logger.exception(f"[{self.name}] Unexpected error in processing loop: {e}")

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
        return f"<Node: {self.name}>"
