import calendar
import datetime
import re
from itertools import product
from typing import Any, Callable, Dict, Iterable


def parse_list(value: str) -> Dict[str, Any]:
    result = re.match(r"\s*(?:[\w\:]+\s*(?:[a|p]m)?)(?:(?:\s*,?\s*|\s+)(?:(?:and|&)\s+)?(?:[\w\:]+\s*(?:[a|p]m)?))*\s*", value)
    if result:
        return {'list': [w
                         for w in re.findall(r"[\w\:]+(?:\s*[a|p]m)?", value)
                         if w not in ('and',)],
                'len': result.endpos}


def parse_range(value: str) -> Dict[str, Any]:
    result = re.match(r"\s*(?:from\s+)?(?P<start>[\w\:]+)\s*(?:to|through|-)\s*(?P<end>[\w\:]+)\s*", value)
    if result:
        return {'start': result['start'],
                'end': result['end'],
                'len': len(result[0])}


def parse_interval(value: str) -> Dict[str, Any]:
    result = re.match(r"\s*every\s+(?:(?P<interval>\d+)\s*)?(?:(?P<interval_type>\w+)\s*)?", value)
    if result:
        dict_ = result.groupdict()
        return {'interval': int(dict_['interval']) if dict_['interval'] else dict_['interval'],
                'interval_type': dict_.get('interval_type'),
                'len': len(result[0])}


def parse_phrase(value: str, iterate: Callable, parse: Callable):
    range_ = parse_range(value)
    if range_:
        interval = parse_interval(value[range_['len']:])
        return iterate(range_, interval)
    interval = parse_interval(value)
    if interval:
        range_ = parse_range(value[interval['len']:])
        return iterate(range_, interval)
    return [parse(d) for d in parse_list(value)['list']]


def parse_day(value: str) -> int:
    days = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
    if value in days:
        return days.index(value[:2])


def parse_time(value: str) -> Dict[str, int]:
    result = re.match(r"\s*(?P<hour>\d{1,2})\s*:\s*(?P<minute>\d{1,2})\s*(?P<ampm>[a|p]m)?", value)
    if result:
        dict_ = result.groupdict()
        hour = int(dict_['hour'])
        minute = int(dict_['minute']) if 'minute' in dict_ else 0
        second = 0  # todo add seconds schedule_parsing?
        if dict_['ampm']:
            hour += \
                12 if dict_['ampm'][0] == 'p' and hour != 12 else \
                -12 if dict_['ampm'][0] == 'a' and hour == 12 else \
                0
        return {'hour': hour, 'minute': minute}


def iterate_days(range_, interval) -> Iterable[int]:
    # todo other intervals?
    start = parse_day(range_['start'])
    end = parse_day(range_['end'])
    if end < start:
        end += 7
    return [d % 7 for d in range(start, end + 1)]


def iterate_times(range_, interval) -> Iterable[Dict[str, Any]]:
    start = parse_time(range_['start']) if range_ else {'hour': 0, 'minute': 0}
    end = parse_time(range_['end']) if range_ else {'hour': 23, 'minute': 59}
    hour_delta = 0
    minute_delta = 0
    if end['hour'] < start['hour']:  # todo minutes?
        end['hour'] += 24
    interval_ = interval['interval'] or 1
    interval_type = interval['interval_type'] or 'hours'
    while (start['hour'] + hour_delta) * 60 + (start['minute'] + minute_delta) <= end['hour'] * 60 + end['minute']:
        yield {'hour': (start['hour'] + hour_delta) % 24, 'minute': (start['minute'] + minute_delta) % 60}
        if interval_type in ('minute', 'minutes'):
            minute_delta += interval_
            hour_delta += minute_delta // 60
            minute_delta %= 60
        elif interval_type in ('hour', 'hours'):
            hour_delta += interval_
        else:
            raise Exception("interval type not recognized")


def end_of_month():
    # todo not just this year
    now = datetime.datetime.now()
    return calendar.monthrange(now.year, now.month)[1]


def parse_day_phrase(phrase) -> Iterable[Dict[str, Any]]:
    match = re.match(r'\s*(?:day\s+of\s+month|dom)\s+(?P<start>\d+)\s+(?:to|through|-)\s+(?P<end>\d+)', phrase)
    if match:
        start = int(match['start'])
        end = int(match['end'])
        if end < start:
            return [{'dom': _} for _ in [*range(int(match['start']), end_of_month()), *range(1, int(match['end'])+1)]]
        return [{'dom': _} for _ in range(start, end + 1)]
    match = re.match(r'\s*(?:every\s*days?|daily)\s*', phrase)
    if match:
        return [{'weekday': _} for _ in range(7)]
    match = re.match(r'\s*week\s*days?\s*', phrase)
    if match:
        return [{'weekday': _} for _ in range(1, 6)]
    match = re.match(r'\s*week\s*ends?\s*', phrase)
    if match:
        return [{'weekday': _} for _ in (0, 6)]
    return [{'weekday': _} for _ in parse_phrase(phrase, iterate_days, parse_day)]


def parse_time_phrase(phrase):
    return parse_phrase(phrase, iterate_times, parse_time)


def parse_complex_phrase(phrase):
    result = re.match(r'(?P<day_phrase>.+?)\s*(?:at|@)\s*(?P<time_phrase>.+)', phrase)
    if result:
        return [{**dp, **tp}
                for dp, tp
                in product(parse_day_phrase(result['day_phrase']),
                           parse_time_phrase(result['time_phrase']))]
    result = parse_time_phrase(phrase)
    if result:
        return result
