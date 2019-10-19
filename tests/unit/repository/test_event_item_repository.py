import pytest

from savoten.domain import Candidate, EventItem, User
from savoten.repository.memory import EventItemRepository
from tests.util import get_public_vars

user_args = {
    'name': 'test_user',
    'email': 'test_user@test.com',
    'permission': 100
}
user = User(**user_args)
candidate_args = {'user': user}
candidate = Candidate(**candidate_args)

class TestSave:

    def setup_method(self, method):
        print('\n### setup_method {} ###'.format(method.__name__))
        self.repository = EventItemRepository()
        print('vars(repository): {}' .format(vars(self.repository)))

    def teardown_method(self, method):
        print('\n### teardown_method {} ###'.format(method.__name__))
        print('vars(repository): {}' .format(vars(self.repository)))

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate])])
    def test_succeeds_when_given_event_item_has_no_id(self, event_item):
        self.repository.save(event_item)
        assert get_public_vars(
            self.repository.event_items[1]) == get_public_vars(event_item)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=3)])
    def test_update_succeeds_when_given_event_item_has_id(
            self, event_item):
        self.repository.save(event_item)
        event_item.name = 'updated_name'
        self.repository.save(event_item)
        assert get_public_vars(
            self.repository.event_items[3]) == get_public_vars(event_item)

class TestDelete:

    def setup_method(self, method):
        print('\n### setup_method {} ###'.format(method.__name__))
        self.repository = EventItemRepository()
        self.repository.event_items[1] = [EventItem('test_name', [candidate], id=1)]
        print('vars(repository): {}' .format(vars(self.repository)))

    def teardown_method(self, method):
        print('\n### teardown_method {} ###'.format(method.__name__))
        print('vars(repository): {}' .format(vars(self.repository)))

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=1)])
    def test_succeeds_when_target_event_item_exists(self, event_item):
        self.repository.delete(event_item)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name2', [candidate], id=2)])
    def test_return_value_error_when_target_event_item_does_not_exist(
            self, event_item):
        with pytest.raises(ValueError):
            assert self.repository.delete(event_item)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=None)])
    def test_return_value_error_when_given_event_item_id_is_none(self, event_item):
        with pytest.raises(ValueError):
            assert self.repository.delete(event_item)

class TestFindById:

    @classmethod
    def setup_class(cls):
        print('\n### setup_class {} ###'.format(cls.__name__))
        cls.repository = EventItemRepository()
        cls.repository.event_items[1] = EventItem('test_name', [candidate], id=1)
        print('vars(repository): {}' .format(vars(cls.repository)))

    @classmethod
    def teardown_class(cls):
        print('\n### teardown_class {} ###'.format(cls.__name__))
        print('vars(repository): {}' .format(vars(cls.repository)))

    def test_return_event_item_when_target_id_exists(self):
        assert get_public_vars(self.repository.find_by_id(1)) == get_public_vars(
            self.repository.event_items[1])

    def test_return_none_if_target_id_does_not_exist(self):
        assert self.repository.find_by_id(100) is None

class TestFindByEventId:

    @classmethod
    def setup_class(cls):
        print('\n### setup_class {} ###'.format(cls.__name__))
        cls.repository = EventItemRepository()
        cls.added_event_items = []
        event_id = 1
        cls.repository.event_id_to_event_item_map[event_id] = []
        for i in range(1, 5):
            event_item = EventItem('test_name', [candidate], id=i)
            cls.repository.event_id_to_event_item_map[event_id].append(event_item)
            cls.added_event_items.append(event_item)
        print('vars(repository): {}' .format(vars(cls.repository)))

    @classmethod
    def teardown_class(cls):
        print('\n### teardown_class {} ###'.format(cls.__name__))
        print('vars(repository): {}' .format(vars(cls.repository)))

    def test_return_found_event_items_when_target_event_id_exists(self):
        assert set(self.repository.find_by_event_id(1)) == set(self.added_event_items)

    def test_return_none_when_target_event_item_does_not_exist(self):
        assert self.repository.find_by_event_id(2) is None
