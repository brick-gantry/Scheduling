from datetime import datetime, timedelta
from typing import Iterable

from src.tasks.schedule_parsing.chronitization import chronitize
from src.tasks.schedule_parsing.parsing import parse_complex_phrase


def parse_schedule(schedule: str, lookahead=timedelta(days=1), now=None) -> Iterable[datetime]:
    return chronitize(parse_complex_phrase(schedule), lookahead, now)
