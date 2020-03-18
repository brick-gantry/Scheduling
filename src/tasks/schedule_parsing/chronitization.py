from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List


def _get_now(now=None):
    return now or datetime.now()


def chronitize(parsed_schedules: List[Dict[str, Any]], lookahead=timedelta(days=1), now=None) -> Iterable[datetime]:
    now = _get_now(now)
    for ps in parsed_schedules:
        def iterate_days():
            output = now
            while output <= now + lookahead:
                if 'weekday' in ps:
                    if output.weekday() == ps['weekday']:
                        yield output
                elif 'dom' in ps:
                    if output.day == ps['dom']:
                        yield output
                else:
                    yield output
                output += timedelta(days=1)

        for day in iterate_days():
            day = day.replace(hour=ps.get('hour', 0), minute=ps.get('minute', 0), second=ps.get('second_offset', 0))
            day += timedelta(minutes=ps.get('minute_offset', 0), seconds=ps.get('seconds_offset', 0))
            if now <= day <= now + lookahead:
                yield day
