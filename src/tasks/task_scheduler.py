from datetime import datetime
from typing import Callable, Dict, Iterable, Tuple

from src.tasks.task import Task


class TaskScheduler:
    def __init(self):
        self._tasks: Dict[int, Task] = {t.idx: t for t in Task.read_many()}
        self._scheduled_tasks: Iterable[Tuple[datetime, Task]] = []
        self._schedule()

    def _schedule(self):
        self._scheduled_tasks = list(sorted([(scheduled_datetime, task)
                                             for task in self._tasks.values()
                                             for scheduled_datetime in task.refresh_schedule()]))

    def _process_before(self, target_time: datetime, callback: Callable):
        to_process, self._scheduled_tasks = [st for st in self._scheduled_tasks if st[0] > target_time]
        for st in to_process:
            if st[0] <= target_time:
                callback(st[1])

    def create(self, task_def):
        t = Task(**task_def)
        t.create()
        self._tasks[t.idx] = t
        self._schedule()

    def update(self, task_id, task_def):
        t = self._tasks[task_id]
        for k, v in task_def.items():
            setattr(t, k, v)
        t.update()
        self._schedule()

    def delete(self, task_id):
        Task.delete(task_id)
        del self._tasks[task_id]
        self._schedule()


