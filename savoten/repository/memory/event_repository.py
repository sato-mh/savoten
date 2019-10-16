from savoten import domain


class EventRepository(domain.EventRepositoryInterface):

    def __init__(self):
        self.events = {}
        self.id = 0

    def save(self, event):
        if event.id is None:
            event.id = self.get_new_id()
        self.events[event.id] = event
        return event

    def delete(self, event):
        if event.id is None or event.id not in self.events:
            raise ValueError("error!")
        self.events.pop(event.id)

    def find_by_id(self, id):
        id = int(id)
        return self.events.get(id)

    def find_all(self):
        return self.events

    def get_new_id(self):
        self.id = self.id + 1
        return self.id
