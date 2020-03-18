import time
from datetime import datetime
from threading import Thread

from src.tasks.task import Task
from src.tasks.task_scheduler import TaskScheduler


def _default_subprocess_reader(proc_stream, local_stream):
    for line in iter(proc_stream.readline, b''):
        local_stream.write(line.decode('utf-8'))


class TaskExecutor(TaskScheduler):
    def __init__(self):
        super().__init__()
        self._t = None

    def run(self, sleep_interval=.1) -> Thread:
        def p():
            while True:
                self._process_before(datetime.now(), lambda task: task.execute())
                time.sleep(sleep_interval)
        self._t = Thread(target=p)
        self._t.daemon = True
        self._t.start()
        return t
