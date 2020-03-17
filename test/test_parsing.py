
import pytest
import src.schedule_parsing as parsing


@pytest.mark.parametrize(['value', 'result'],
                         [('a, b, c', {'list': ['a', 'b', 'c'], 'len': 7}),
                          ('a, b, and c', {'list': ['a', 'b', 'c'], 'len': 11}),
                          ('a b and c', {'list': ['a', 'b', 'c'], 'len': 9}),
                          ('a, b, & c', {'list': ['a', 'b', 'c'], 'len': 9}),
                          ('a    b   c', {'list': ['a', 'b', 'c'], 'len': 10}),
                          (' a, b, c ', {'list': ['a', 'b', 'c'], 'len': 9}),
                          ('larry, moe and curly', {'list': ['larry', 'moe', 'curly'], 'len': 20}),
                          ])
def test_parse_list(value, result):
    assert parsing.parse_list(value) == result


def test_parse_list_failures():
    assert parsing.parse_list('') is None


@pytest.mark.parametrize(['value', 'result'],
                         [('a to b', {'start': 'a', 'end': 'b', 'len': 6}),
                          ('a through b', {'start': 'a', 'end': 'b', 'len': 11}),
                          ('a-b', {'start': 'a', 'end': 'b', 'len': 3}),
                          ('a - b', {'start': 'a', 'end': 'b', 'len': 5}),
                          (' a to b ', {'start': 'a', 'end': 'b', 'len': 8}),
                          (' from a to b', {'start': 'a', 'end': 'b', 'len': 12}),
                          ('east to west', {'start': 'east', 'end': 'west', 'len': 12})
                          ])
def test_parse_range(value, result):
    assert parsing.parse_range(value) == result


def test_parse_range_failure():
    assert parsing.parse_range('a b') is None


@pytest.mark.parametrize(['value', 'result'],
                         [('every 10 minutes', {'interval': 10, 'interval_type': 'minutes', 'len': 16}),
                          ('every 10', {'interval': 10, 'interval_type': None, 'len': 8}),
                          ('every minute', {'interval': None, 'interval_type': 'minute', 'len': 12}),
                          ])
def test_parse_interval(value, result):
    assert parsing.parse_interval(value) == result


def test_parse_interval_failure():
    assert parsing.parse_interval('') is None


@pytest.mark.parametrize(['value', 'result'],
                         [(we, idx)
                          for we, idx
                          in zip(['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su'], range(7))
                          ])
def test_parse_day(value, result):
    assert parsing.parse_day(value) == result


def test_parse_day_failure():
    assert parsing.parse_day('bl') is None


@pytest.mark.parametrize(['value', 'result'],
                         [('a to c', ['a', 'b', 'c']),
                          ('a to e every 2', ['a', 'c', 'e']),
                          ('every 2 letters a to e', ['a', 'c', 'e']),
                          ('every 2', ['a', 'c', 'e', 'g']),
                          ('a, b, c', ['a', 'b', 'c'])])
def test_parse_phrase(value, result):
    def iterate_char(range, interval):
        start = range['start'] if range else 'a'
        end = range['end'] if range else 'h'
        interval = interval['interval'] if interval else 1
        while start <= end:
            yield start
            start = chr(ord(start[0])+(interval if interval else 1))
    assert list(parsing.parse_phrase(value, iterate_char, lambda x: x)) == result


# def test_parse_phrase_fail():
#     raise NotImplementedError()


@pytest.mark.parametrize(['value', 'result'],
                         [('12:00 am', {'hour': 0, 'minute': 0}),
                          ('12:01 am', {'hour': 0, 'minute': 1}),
                          ('2:00 am', {'hour': 2, 'minute': 0}),
                          ('12:00 pm', {'hour': 12, 'minute': 0}),
                          ('12:01 pm', {'hour': 12, 'minute': 1}),
                          ('2:00 pm', {'hour': 14, 'minute': 0}),
                          ('11:59 pm', {'hour': 23, 'minute': 59}),
                          ('14:37', {'hour': 14, 'minute': 37})
                          ])
def test_parse_time(value, result):
    assert parsing.parse_time(value) == result


# def test_parse_time_failure():
#     raise NotImplementedError()


@pytest.mark.parametrize(['range', 'interval', 'result'],
                         [({'start': 'mo', 'end': 'we'}, None, [0, 1, 2]),
                          ({'start': 'fr', 'end': 'mo'}, None, [4, 5, 6, 0]),
                          ])
def test_iterate_days(range, interval, result):
    assert list(parsing.iterate_days(range, interval)) == result


# def test_parse_iterate_days_failure():
#     raise NotImplementedError()


@pytest.mark.parametrize(['range', 'interval', 'result'],
                         [({'start': '01:00', 'end': '03:00'}, {'interval': 30, 'interval_type': 'minutes'},
                           [{'hour': 1, 'minute': 0}, {'hour': 1, 'minute': 30},
                            {'hour': 2, 'minute': 0}, {'hour': 2, 'minute': 30},
                            {'hour': 3, 'minute': 0}
                            ]),
                          ({'start': '01:00', 'end': '03:00'}, {'interval': 1, 'interval_type': 'hours'},
                           [{'hour': 1, 'minute': 0}, {'hour': 2, 'minute': 0}, {'hour': 3, 'minute': 0}
                            ]),
                          ({'start': '23:00', 'end': '01:00'}, {'interval': 30, 'interval_type': 'minutes'},
                           [{'hour': 23, 'minute': 0}, {'hour': 23, 'minute': 30},
                            {'hour': 0, 'minute': 0}, {'hour': 0, 'minute': 30},
                            {'hour': 1, 'minute': 0}
                            ]),
                          ({'start': '23:00', 'end': '01:00'}, {'interval': 1, 'interval_type': 'hours'},
                           [{'hour': 23, 'minute': 0},  {'hour': 0, 'minute': 0}, {'hour': 1, 'minute': 0}
                            ])
                          ])
def test_iterate_times(range, interval, result):
    assert list(parsing.iterate_times(range, interval)) == result


# def test_iterate_times_failure():
#     raise NotImplementedError()


@pytest.mark.parametrize(['phrase', 'result'],
                         [('every day', [{'weekday': _} for _ in [0, 1, 2, 3, 4, 5, 6]]),
                          ('daily', [{'weekday': _} for _ in [0, 1, 2, 3, 4, 5, 6]]),
                          ('week days', [{'weekday': _} for _ in [1, 2, 3, 4, 5]]),
                          ('weekends', [{'weekday': _} for _ in [0, 6]]),
                          ('tu - sa', [{'weekday': _} for _ in [1, 2, 3, 4, 5]]),
                          ('we', [{'weekday': _} for _ in [2]]),
                          ('day of month 1 through 5', [{'dom': _} for _ in [1, 2, 3, 4, 5]]),
                          ('day of month 28 - 3', [{'dom': _} for _ in [*range(28, parsing.end_of_month()), 1, 2, 3]])
                          ])
def test_parse_day_phrase(phrase, result):
    assert list(parsing.parse_day_phrase(phrase)) == result


@pytest.mark.parametrize(['phrase', 'result'],
                         [('6:30 pm', [{'hour': 18, 'minute': 30}]),
                          ('16:00, 19:45', [{'hour': 16, 'minute': 0},
                                            {'hour': 19, 'minute': 45}]),
                          ('16:00 to 18:00 every hour', [{'hour': 16, 'minute': 0},
                                                         {'hour': 17, 'minute': 0},
                                                         {'hour': 18, 'minute': 0}])
                          ])
def test_parse_time_phrase(phrase, result):
    assert list(parsing.parse_time_phrase(phrase)) == result


@pytest.mark.parametrize(['phrase', 'result'],
                         [('weekdays at 18:00 and 21:00', [{'weekday': 1, 'hour': 18, 'minute': 0},
                                                           {'weekday': 1, 'hour': 21, 'minute': 0},
                                                           {'weekday': 2, 'hour': 18, 'minute': 0},
                                                           {'weekday': 2, 'hour': 21, 'minute': 0},
                                                           {'weekday': 3, 'hour': 18, 'minute': 0},
                                                           {'weekday': 3, 'hour': 21, 'minute': 0},
                                                           {'weekday': 4, 'hour': 18, 'minute': 0},
                                                           {'weekday': 4, 'hour': 21, 'minute': 0},
                                                           {'weekday': 5, 'hour': 18, 'minute': 0},
                                                           {'weekday': 5, 'hour': 21, 'minute': 0}
                                                           ])
                          ])
def test_parse_full_phrase(phrase, result):
    assert list(parsing.parse_full_phrase(phrase)) == result

