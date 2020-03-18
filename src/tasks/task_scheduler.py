from datetime import datetime
from typing import Callable, Iterable, Tuple

from src.tasks.task import Task
from src.tasks.task_persistence import TaskPersistence


class TaskScheduler(TaskPersistence):
    def __init(self):
        super().__init__()
        self._scheduled_tasks: Iterable[Tuple[datetime, Task]] = []
        self._schedule()

    def _schedule(self):
        self._scheduled_tasks = list(sorted([(scheduled_datetime, task)
                                             for task in self._tasks
                                             for scheduled_datetime in task.refresh_schedule()]))

    def _process_before(self, target_time: datetime, callback: Callable):
        to_process, self._scheduled_tasks = [st for st in self._scheduled_tasks if st[0] > target_time]
        for st in to_process:
            if st[0] <= target_time:
                callback(st[1])

    def create(self, task):
        super().create(task)
        self._schedule()

    def update(self, task_id, task):
        super().update(task_id, task)
        self._schedule()

    def delete(self, task_id):
        super().create(task_id)
        self._schedule()


