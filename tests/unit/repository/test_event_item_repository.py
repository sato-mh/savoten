import pytest
from savoten.domain import EventItem, Candidate, User
from savoten.repository.memory import EventItemRepository


# 頻繁に使用する変数のsetup
@pytest.fixture(scope='function', autouse=True)
def setup_typical_params():
    user_args = {'name':'test_user', 'email':'test_user@example.com', 'permission':100}
    user = User(**user_args)
    candidate_args = {'user':user, 'description':'test_candidate'}
    candidate = Candidate(**candidate_args)
    candidates = [candidate]
    event_item_args = {'name':'Leader', 'candidates':candidates, 'description':'test_event'}
    event_item = EventItem(**event_item_args)
    event_item_repository = EventItemRepository()
    typical_params = {
        'event_item':event_item,
        'event_item_repository': event_item_repository
    }
    return typical_params

class TestSave:

    def test_save_suceeded_when_event_item_id_is_none(self, setup_typical_params):
        event_item_repository = setup_typical_params['event_item_repository']
        event_item_repository.save(setup_typical_params['event_item'])

    def test_save_suceeded_when_event_item_id_exists(self, setup_typical_params):
        event_item_repository = setup_typical_params['event_item_repository']
        event_item_id_exist = event_item_repository.save(setup_typical_params['event_item'])
        description = 'This event_item.id=1'
        event_item_id_exist.description = description
        event_item_repository.save(event_item_id_exist)
        assert event_item_repository.event_items[event_item_id_exist.id].description == description

class TestDelete:
    def test_delete_suceeded_when_event_item_exists(self, setup_typical_params):
        event_item_repository = setup_typical_params['event_item_repository']
        event_item = setup_typical_params['event_item']
        event_item.id = 1
        event_item_repository.event_items['1'] = event_item
        event_item_repository.delete(event_item)

    def test_delete_failure_when_event_item_id_is_none(self, setup_typical_params):
        event_item_repository = setup_typical_params['event_item_repository']
        event_item = setup_typical_params['event_item']
        event_item.id = None
        with pytest.raises(ValueError):
            assert event_item_repository.delete(event_item)

    def test_delete_failure_when_event_item_is_not_exist(self, setup_typical_params):
        event_item_repository = setup_typical_params['event_item_repository']
        event_item = setup_typical_params['event_item']
        event_item.id = 1
        with pytest.raises(ValueError):
            assert event_item_repository.delete(event_item)

