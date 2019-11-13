import pytest

from savoten.domain import User
from savoten.repository.memory import UserRepository
from tests.util import get_public_vars

user_args = {
    'name': 'test_user',
    'email': 'test_user@test.com',
    'permission': 100
}


class TestSave:

    def setup_method(self):
        self.repository = UserRepository()

    @pytest.mark.parametrize('user', [User(**user_args)])
    def test_succeeds_when_user_has_no_id(self, user):
        saved_user = self.repository.save(user)
        assert get_public_vars(
            self.repository.users[saved_user.id]) == get_public_vars(user)

    @pytest.mark.parametrize(
        'user, updated_user',
        [(User(**user_args),
          User(name='updated', email='test_user@test.com', permission=100))])
    def test_update_succeeds_when_user_has_same_id(self, user, updated_user):
        saved_user = self.repository.save(user)
        user_id = saved_user.id
        updated_user.id = user_id
        self.repository.save(updated_user)
        assert get_public_vars(
            self.repository.users[user_id]) == get_public_vars(updated_user)


class TestDelete:

    @classmethod
    def setup_class(cls):
        cls.repository = UserRepository()
        cls.repository.users[1] = User(**user_args, id=1)

    @pytest.mark.parametrize('user', [User(**user_args, id=1)])
    def test_succeeds_when_target_user_exists(self, user):
        self.repository.delete(user)

    @pytest.mark.parametrize('user', [User(**user_args, id=100)])
    def test_return_value_error_when_target_user_does_not_exist(self, user):
        with pytest.raises(ValueError):
            assert self.repository.delete(user)

    @pytest.mark.parametrize('user', [User(**user_args, id=None)])
    def test_return_value_error_when_given_user_id_is_none(self, user):
        with pytest.raises(ValueError):
            assert self.repository.delete(user)


class TestFindById:

    @classmethod
    def setup_class(cls):
        cls.repository = UserRepository()
        cls.repository.users[1] = User(**user_args, id=1)

    def test_return_user_when_target_id_exists(self):
        assert get_public_vars(
            self.repository.find_by_id(1)) == get_public_vars(
                self.repository.users[1])

    def test_return_none_when_target_id_does_not_exist(self):
        assert self.repository.find_by_id(100) is None


class TestFindAll:

    @classmethod
    def setup_class(cls):
        cls.repository = UserRepository()
        cls.test_users = [User(**user_args, id=i) for i in range(1, 5)]
        for user in cls.test_users:
            cls.repository.users[user.id] = user

    def test_return_all_user(self):
        assert set(self.repository.find_all()) == set(self.test_users)
