import pytest

from savoten.domain import Candidate, User
from tests.util import get_public_vars

user = User('user_name', 'email@test.com', 1)
user2 = User('user_name2', 'email2@test.com', 2)

class TestInit:

    @pytest.mark.parametrize('valid_args, expected', [
        ({
            'id': 1,
            'user': user,
            'description': 'description for test'
        }, {
            'id': 1,
            'user': user,
            'description': 'description for test'
        }),
        ({
            'user': user,
        }, {
            'id': None,
            'user': user,
            'description': None
        })
    ])
    def test_succeeds_initialization_with_valid_args(self, valid_args, expected):
        candidate = Candidate(**valid_args)
        assert get_public_vars(candidate) == expected

    @pytest.mark.parametrize('invalid_args', [
        {
            'user': 'user'
        }
    ])
    def test_raise_type_error_with_invalid_args(self, invalid_args):
        with pytest.raises(TypeError):
            Candidate(**invalid_args)

candidate = Candidate(user, id = 1)
print(vars(candidate))
print(candidate.user)
print("123")
print(candidate.id)
candidate.user = user2
print("hoge")
print(candidate.user.name)
print(vars(candidate))
