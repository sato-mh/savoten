import datetime

import pytest

from savoten.domain import Period

now = datetime.datetime.now()
one_day_ago = now - datetime.timedelta(days=1)
one_day_later = now + datetime.timedelta(days=1)
two_days_later = now + datetime.timedelta(days=2)


class TestInit:

    @pytest.mark.parametrize('valid_args', [
        {
            'start': now,
            'end': one_day_later
        },
        {
            'start': one_day_ago,
            'end': now
        }
    ])
    def test_init_period_with_valid_args(self, valid_args):
        Period(valid_args['start'], valid_args['end'])

    @pytest.mark.parametrize('invalid_args', [
        {
            'start': now.isoformat(),
            'end': one_day_later
        },
        {
            'start': now,
            'end': one_day_later.isoformat()
        },
    ])
    def test_init_period_with_invalid_args(self, invalid_args):
        with pytest.raises(TypeError):
            Period(invalid_args['start'], invalid_args['end'])


class TestIsWithin:

    @pytest.mark.parametrize('context', [
        {
            'start': now,
            'end': one_day_later
        }
    ])
    def test_return_true_when_in_the_period(self, context):
        in_period = Period(context['start'], context['end'])
        assert in_period.is_within() is True

    @pytest.mark.parametrize('context', [
        {
            'start': one_day_ago,
            'end': now
        },
        {
            'start': one_day_later,
            'end': two_days_later
        },
    ])
    def test_return_false_when_outside_the_period(self, context):
        outside_period = Period(context['start'], context['end'])
        assert outside_period.is_within() is False
