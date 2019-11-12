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

    def setup_method(self):
        self.repository = EventItemRepository()

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate])])
    def test_succeeds_when_event_item_has_no_id(self, event_item):
        saved_event_item = self.repository.save(event_item)
        assert get_public_vars(self.repository.event_items[
            saved_event_item.id]) == get_public_vars(event_item)

    @pytest.mark.parametrize('event_item, updated_event_item', [(EventItem(
        'test_name', [candidate]), EventItem('updated', [candidate]))])
    def test_update_succeeds_when_event_item_has_same_id(
            self, event_item, updated_event_item):
        saved_event_item = self.repository.save(event_item)
        updated_event_item.id = saved_event_item.id
        self.repository.save(updated_event_item)
        assert get_public_vars(self.repository.event_items[
            saved_event_item.id]) == get_public_vars(updated_event_item)


class TestDelete:

    def setup_method(self):
        self.repository = EventItemRepository()
        self.repository.event_items[1] = [
            EventItem('test_name', [candidate], id=1)
        ]

    @pytest.fixture()
    def regist_event_item_to_event_id_map(self):
        event_id = 1
        event_item = EventItem('test_name', [candidate], id=1)
        self.repository.event_id_to_event_item_map[event_id] = [event_item]

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=1)])
    def test_succeeds_when_target_event_item_exists(self, event_item):
        self.repository.delete(event_item)

    @pytest.mark.parametrize('event_item, event_id',
                             [(EventItem('test_name', [candidate], id=1), 1)])
    def test_succeeds_when_target_event_item_registerd_in_event_id_map(
            self, event_item, event_id, regist_event_item_to_event_id_map):
        self.repository.delete(event_item)
        for registed_event_items in self.repository.event_id_to_event_item_map.values(
        ):
            for registed_event_item in registed_event_items:
                assert event_item.id == registed_event_item.id

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name2', [candidate], id=2)])
    def test_return_value_error_when_target_event_item_does_not_exist(
            self, event_item):
        with pytest.raises(ValueError):
            assert self.repository.delete(event_item)

    @pytest.mark.parametrize('event_item',
                             [EventItem('test_name', [candidate], id=None)])
    def test_return_value_error_when_given_event_item_id_is_none(
            self, event_item):
        with pytest.raises(ValueError):
            assert self.repository.delete(event_item)


class TestFindById:

    @classmethod
    def setup_class(cls):
        cls.repository = EventItemRepository()
        cls.repository.event_items[1] = EventItem('test_name', [candidate],
                                                  id=1)

    def test_return_event_item_when_target_id_exists(self):
        assert get_public_vars(
            self.repository.find_by_id(1)) == get_public_vars(
                self.repository.event_items[1])

    def test_return_none_if_target_id_does_not_exist(self):
        assert self.repository.find_by_id(100) is None


class TestFindByEventId:

    @classmethod
    def setup_class(cls):
        cls.repository = EventItemRepository()
        cls.test_event_items = [
            EventItem('test_name', [candidate], id=i) for i in range(1, 5)
        ]
        event_id = 1
        cls.repository.event_id_to_event_item_map[
            event_id] = cls.test_event_items

    def test_return_found_event_items_when_target_event_id_exists(self):
        assert set(self.repository.find_by_event_id(1)) == set(
            self.test_event_items)

    def test_return_none_when_target_event_item_does_not_exist(self):
        assert self.repository.find_by_event_id(2) is None
