import datetime

import pytest

from savoten.domain import Event, Period
from savoten.repository.memory.event_repository import EventRepository
from tests.util import get_public_vars

event_args = {
    'name':
        'test_event',
    'items': [],
    'period':
        Period(start=datetime.date(1970, 1, 1), end=datetime.date(2038, 1, 19)),
}


class TestSave:

    def setup_method(self):
        self.repository = EventRepository()

    @pytest.mark.parametrize('event', [Event(**event_args)])
    def test_create_succeeds_when_event_has_no_id(self, event):
        saved_event = self.repository.save(event)
        assert get_public_vars(
            self.repository.events[saved_event.id]) == get_public_vars(event)

    @pytest.mark.parametrize('event, updated_event',
                             [(Event(name=event_args['name'],
                                     items=event_args['items'],
                                     period=event_args['period']),
                               Event(name='updated',
                                     items=event_args['items'],
                                     period=event_args['period']))])
    def test_update_succeeds_when_event_has_exist_id(self, event,
                                                     updated_event):
        saved_event = self.repository.save(event)
        event_id = saved_event.id
        print(event_id)
        updated_event.id = event_id
        self.repository.save(updated_event)
        assert get_public_vars(
            self.repository.events[event_id]) == get_public_vars(updated_event)


class TestDelete:

    def setup_method(self):
        self.repository = EventRepository()
        self.saved_event = self.repository.save(Event(**event_args))

    @pytest.mark.parametrize('event', [Event(**event_args)])
    def test_succeeds_when_target_event_item_exists(self, event):
        self.repository.delete(self.saved_event)


class TestFindById:

    def setup_method(self):
        self.repository = EventRepository()
        self.saved_event = self.repository.save(Event(**event_args))

    def test_return_found_event_when_target_event_id_exists(self):
        assert self.repository.find_by_id(
            self.saved_event.id) == self.saved_event


class TestFindAll:

    def setup_method(self):
        self.repository = EventRepository()
        self.saved_events = list()
        self.saved_events.append(self.repository.save(Event(**event_args)))
        self.saved_events.append(self.repository.save(Event(**event_args)))

    def test_find_all(self):
        assert len(self.saved_events) == len(self.repository.find_all())
