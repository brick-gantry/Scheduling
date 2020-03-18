from src.tasks.task import Task

# todo nonlocal persistence
# todo shared cache


class TaskPersistence:
    def __init__(self):
        self._tasks = {}
        self._task_sequence = 0

    def create(self, task):
        self._tasks[self._task_sequence] = task
        self._task_sequence += 1

    def read(self):
        return list(self._tasks.values())

    def _read_from_cache(self):
        try:
            raise NotImplementedError()
        except:
            self._read_from_database()

    def _read_from_database(self):
        try:
            raise NotImplementedError()
        except:
            raise NotImplementedError()

    def update(self, task_id, task):
        self._tasks[task_id] = {**self._tasks[task_id], **task}

    def delete(self, task_id):
        del self._tasks[task_id]
