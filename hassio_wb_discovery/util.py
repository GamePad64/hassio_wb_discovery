import asyncio
from asyncio.tasks import Task
from typing import Any, Iterable


class Tree(dict):
    def __missing__(self, key: Any) -> Any:
        value = self[key] = type(self)()
        return value


async def cancel_tasks(tasks: Iterable[Task]) -> None:
    for task in tasks:
        if task.done():
            continue
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
