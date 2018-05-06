import datetime

import pytest

from savoten import domain


class TestPeriod:

    NOW = datetime.datetime.now()

    @pytest.fixture(
        scope='function',
        params=[
            {
                'start': NOW,
                'end': NOW + datetime.timedelta(hours=1)
            },
            {
                'start': NOW - datetime.timedelta(hours=1),
                'end': NOW
            }
        ]
    )
    def valid_init_args(self, request):
        return request.param

    def test_init_period_with_valid_args(self, valid_init_args):
        domain.Period(valid_init_args['start'], valid_init_args['end'])

    @pytest.fixture(
        scope='function',
        params=[
            {
                'start': NOW.isoformat(),
                'end': NOW + datetime.timedelta(hours=1)
            },
            {
                'start': NOW,
                'end': (NOW + datetime.timedelta(hours=1)).isoformat()
            },
        ]
    )
    def invalid_init_args(self, request):
        return request.param

    def test_init_period_with_invalid_args(self, invalid_init_args):
        with pytest.raises(TypeError):
            domain.Period(invalid_init_args['start'], invalid_init_args['end'])

    @pytest.fixture(
        scope='function',
        params=[
            {
                'attrs': {
                    'start': NOW,
                    'end': NOW + datetime.timedelta(hours=1)
                },
                'expect': True
            },
            {
                'attrs': {
                    'start': NOW - datetime.timedelta(hours=1),
                    'end': NOW
                },
                'expect': False
            },
        ]
    )
    def is_within_test_case(sffelf, request):
        return request.param

    def test_is_within(self, is_within_test_case):
        attrs = is_within_test_case['attrs']
        expect = is_within_test_case['expect']
        period = domain.Period(attrs['start'], attrs['end'])
        assert period.is_within() is expect


def test_init_event_with_correct_args():
    start = datetime.datetime.now()
    end = start + datetime.timedelta(hours=1)
    args = {
        'name': 'event_name',
        'items': [],
        'period': domain.Period(start, end),
        'description': 'description for test'
    }
    domain.Event(**args)
