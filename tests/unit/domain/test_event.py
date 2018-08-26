import datetime

from savoten.domain import Event, Period


def test_init_event_with_correct_args():
    start = datetime.datetime.now()
    end = start + datetime.timedelta(hours=1)
    args = {
        'name': 'event_name',
        'items': [],
        'period': Period(start, end),
        'description': 'description for test'
    }
    Event(**args)
