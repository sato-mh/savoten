import pytest

from savoten.domain import Candidate, EventItem, User
from tests.util import get_public_vars

user = User('user_name', 'email@test.com', 1)
candidate = Candidate(user)


class TestInit:

    @pytest.mark.parametrize('valid_args, expected',
                             [({
                                 'name': 'name',
                                 'candidates': [candidate],
                                 'description': 'description',
                                 'seats': 2,
                                 'max_choice': 3,
                                 'min_choice': 4,
                                 'id': 5
                             }, {
                                 'name': 'name',
                                 'candidates': [candidate],
                                 'description': 'description',
                                 'seats': 2,
                                 'max_choice': 3,
                                 'min_choice': 4,
                                 'id': 5
                             }),
                              ({
                                  'name': 'name',
                                  'candidates': [candidate]
                              }, {
                                  'name': 'name',
                                  'candidates': [candidate],
                                  'description': None,
                                  'seats': 1,
                                  'max_choice': 1,
                                  'min_choice': 1,
                                  'id': None
                              })])
    def test_succeeds_initialization_with_valid_args(self, valid_args,
                                                     expected):
        event_item = EventItem(**valid_args)
        assert get_public_vars(event_item) == expected

    @pytest.mark.parametrize('invalid_args', [{
        'name': 'name',
        'candidates': candidate
    }, {}])
    def test_raise_type_error_with_invalid_args(self, invalid_args):
        with pytest.raises(TypeError):
            EventItem(**invalid_args)
