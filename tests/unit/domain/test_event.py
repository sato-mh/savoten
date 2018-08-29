import datetime

import pytest

from savoten.domain import Candidate, Event, EventItem, Period, User
from tests.util import get_public_vars

user = User('user_name', 'email@test.com', 1)
candidate = Candidate(user)
event_item = EventItem('event_id_name', [candidate])

now = datetime.datetime.now()
one_day_ago = now - datetime.timedelta(days=1)
one_day_later = now + datetime.timedelta(days=1)
period = Period(one_day_ago, one_day_later)


class TestInitEventItem:

    @pytest.mark.parametrize('valid_args, expected', [
        ({
            'id': 1,
            'name': 'name',
            'items': [event_item],
            'period': period,
            'description': 'description',
            'anonymous': True,
            'created_at': now,
            'updated_at': one_day_later,
            'deleted_at': one_day_later,
        }, {
            'id': 1,
            'name': 'name',
            'period': period,
            'items': [event_item],
            'description': 'description',
            'anonymous': True,
            'created_at': now,
            'updated_at': one_day_later,
            'deleted_at': one_day_later,
        }),
        ({
            'name': 'name',
            'items': [event_item],
            'period': period,
        }, {
            'id': None,
            'name': 'name',
            'items': [event_item],
            'period': period,
            'description': None,
            'anonymous': False,
            'created_at': None,
            'updated_at': None,
            'deleted_at': None,
        })
    ])
    def test_succeeds_initialization_with_valid_args(
            self, valid_args, expected):
        event = Event(**valid_args)
        assert get_public_vars(event) == expected

    @pytest.mark.parametrize('invalid_args', [
        {
            'name': 'name',
            'items': event_item,
        },
        {
            'name': 'name',
            'items': 'event_item',
        },
        {}
    ])
    def test_raise_type_error_with_invalid_args(self, invalid_args):
        with pytest.raises(TypeError):
            EventItem(**invalid_args)

    def test_return_true_when_in_the_period(self):
        in_period = period
        event = Event('name', [event_item], in_period)
        assert event.is_within() is True

    def test_return_false_when_outside_the_period(self):
        two_days_ago = now - datetime.timedelta(days=2)
        outside_period = Period(two_days_ago, one_day_ago)
        event = Event('name', [event_item], outside_period)
        assert event.is_within() is False
