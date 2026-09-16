"""Regression test: the task registry is keyed by task, not by name.

Task names are not unique. CrewSession builds a handler task's name from the session,
the event and the handler function, so the same event firing twice while the first
handler is still running produces two live tasks with identical names. Keyed by name,
the second evicted the first from the registry, and then the first task's done handler
deleted the *second* entry, leaving a running task that current_tasks() never reported.
"""

import asyncio
import unittest

from smallestai.atoms.crew.task_manager import TaskManager, TaskManagerParams

# The shape CrewSession._dispatch builds: f"{session}::{event}::{handler}::handler"
COLLIDING_NAME = "sess::on_message::handle::handler"


class TaskRegistryTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.manager = TaskManager()
        self.manager.setup(TaskManagerParams(loop=asyncio.get_running_loop()))
        self.started = []

    async def _blocks(self):
        try:
            await asyncio.sleep(30)
        except asyncio.CancelledError:
            raise

    async def _finishes(self, done: asyncio.Event):
        await asyncio.sleep(0.01)
        done.set()

    async def _drain(self):
        for task in list(self.manager.current_tasks()):
            await self.manager.cancel_task(task)

    async def test_two_tasks_sharing_a_name_are_both_registered(self):
        first = self.manager.create_task(self._blocks(), name=COLLIDING_NAME)
        second = self.manager.create_task(self._blocks(), name=COLLIDING_NAME)

        registered = self.manager.current_tasks()

        self.assertIn(first, registered)
        self.assertIn(second, registered)
        self.assertEqual(len(registered), 2)
        await self._drain()

    async def test_one_task_finishing_does_not_unregister_its_namesake(self):
        """The case that actually loses a task: the short-lived one completes and its
        done handler removes the entry belonging to the one still running."""
        done = asyncio.Event()
        short = self.manager.create_task(self._finishes(done), name=COLLIDING_NAME)
        still_running = self.manager.create_task(self._blocks(), name=COLLIDING_NAME)

        await done.wait()
        await asyncio.sleep(0)  # let the done callback run

        self.assertTrue(short.done())
        self.assertFalse(still_running.done())
        self.assertIn(still_running, self.manager.current_tasks())
        await self._drain()

    async def test_a_finished_task_is_removed_from_the_registry(self):
        """The fix must not stop the registry from pruning completed tasks."""
        done = asyncio.Event()
        task = self.manager.create_task(self._finishes(done), name="solo")

        await done.wait()
        await asyncio.sleep(0)

        self.assertTrue(task.done())
        self.assertNotIn(task, self.manager.current_tasks())
        self.assertEqual(self.manager.current_tasks(), [])

    async def test_cancel_task_unregisters_it(self):
        task = self.manager.create_task(self._blocks(), name="cancel-me")
        self.assertIn(task, self.manager.current_tasks())

        await self.manager.cancel_task(task)

        self.assertNotIn(task, self.manager.current_tasks())

    async def test_distinct_names_are_unaffected(self):
        a = self.manager.create_task(self._blocks(), name="a")
        b = self.manager.create_task(self._blocks(), name="b")

        self.assertEqual(sorted(t.get_name() for t in self.manager.current_tasks()), ["a", "b"])
        self.assertEqual({a, b}, set(self.manager.current_tasks()))
        await self._drain()


if __name__ == "__main__":
    unittest.main()
