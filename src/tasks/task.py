from datetime import datetime
from typing import Iterable

from src.tasks.schedule_parsing import parse_schedule
from src.tasks.execution import execute_task
from src.redis_object import RedisObject


class Task(RedisObject):
    def __init__(self, name, schedule_phrase, task_phrase):
        super().__init__()
        self._prefix = 'task'
        self.name: str = name
        self.schedule_phrase: str = schedule_phrase
        self._upcoming_schedule_times: Iterable[datetime] = parse_schedule(schedule_phrase)
        self.task_phrase = task_phrase

    def refresh_schedule(self):
        self._upcoming_schedule_times: Iterable[datetime] = parse_schedule(self.schedule_phrase)
        return self._upcoming_schedule_times

    def execute(self):
        execute_task(self.task_phrase)
