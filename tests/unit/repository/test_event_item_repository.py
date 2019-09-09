import pytest
from savoten.domain import EventItem, Candidate, User
from savoten.repository.memory import EventItemRepository

typical_user_args = {'name':'test_user', 'email':'test_user@example.com', 'permission':100}
typical_user = User(**typical_user_args)
typical_candidate_args = {'user':typical_user, 'description':'test_candidate'}
typical_candidate = Candidate(**typical_candidate_args)
typical_candidates = [typical_candidate]
typical_event_item_args = {'name':'Leader', 'candidates':typical_candidates, 'description':'test_event'}
typical_event_item = EventItem(**typical_event_item_args)

@pytest.fixture(scope='function', autouse=True)
def set_up_and_teardown_event_item_repository():
    event_item_repository = EventItemRepository()
    yield(event_item_repository)
    del(event_item_repository)

class TestSave:

    def test_save_suceeded_when_event_item_id_is_none(self, set_up_and_teardown_event_item_repository):
        event_item_repository = set_up_and_teardown_event_item_repository
        event_item = event_item_repository.save(typical_event_item)

    def test_save_suceeded_when_event_item_id_exists(self, set_up_and_teardown_event_item_repository):
        event_item_repository = set_up_and_teardown_event_item_repository
        event_item_id_exist = event_item_repository.save(typical_event_item)
        description = 'This event_item.id=1'
        event_item_id_exist.description = description
        event_item_repository.save(event_item_id_exist)
        assert event_item_repository.event_items[event_item_id_exist.id].description == description

class TestDelete:
    def test_delete_suceeded_when_event_item_exists(self, set_up_and_teardown_event_item_repository):
        event_item_repository = set_up_and_teardown_event_item_repository
        event_item = typical_event_item
        event_item.id = 1
        event_item_repository.event_items['1'] = event_item
        event_item_repository.delete(event_item)

    def test_delete_failure_when_event_item_id_is_none(self, set_up_and_teardown_event_item_repository):
        event_item_repository = set_up_and_teardown_event_item_repository
        event_item = typical_event_item
        event_item.id = None
        with pytest.raises(ValueError):
            assert event_item_repository.delete(event_item)

    def test_delete_failure_when_event_item_is_not_exist(self, set_up_and_teardown_event_item_repository):
        event_item_repository = set_up_and_teardown_event_item_repository
        event_item = typical_event_item
        event_item.id = 1
        with pytest.raises(ValueError):
            assert event_item_repository.delete(event_item)

