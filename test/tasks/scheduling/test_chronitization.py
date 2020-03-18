import pytest
from datetime import datetime, timedelta

from src.tasks.schedule_parsing import chronitize


@pytest.fixture
def now():
    return datetime(2020, 1, 3, 12, 37, 48)


@pytest.mark.parametrize(['parsed_schedule', 'lookahead', 'now', 'result'],
                         [({}, timedelta(days=1), datetime(2020, 1, 3, 12, 37, 48), datetime(2020, 1, 4, 0, 0, 0)),
                          ({'hour': 3, 'minute': 15}, timedelta(days=1), datetime(2020, 1, 3, 12, 37, 48), datetime(2020, 1, 4, 3, 15, 0)),
                          ({'minute_offset': 3, 'second_offset': 15}, timedelta(days=1), datetime(2020, 1, 3, 12, 37, 48), datetime(2020, 1, 4, 0, 3, 15)),
                          ({'weekday': 3}, timedelta(days=7), datetime(2020, 1, 3, 12, 37, 48), datetime(2020, 1, 9, 0, 0, 0)),
                          ({'dom': 7}, timedelta(days=7), datetime(2020, 1, 3, 12, 37, 48), datetime(2020, 1, 7, 0, 0, 0))
                          ])
def test_chronitize(parsed_schedule, lookahead, now, result):
    assert list(chronitize([parsed_schedule], lookahead, now)) == [result]