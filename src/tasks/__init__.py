from threading import Thread

from src.tasks.task_executor import TaskExecutor


def boot_tasking_system() -> Thread:
    te = TaskExecutor()
    return te.run()
