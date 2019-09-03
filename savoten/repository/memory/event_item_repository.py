from savoten import domain


class EventItemRepository(domain.EventItemRepositoryInterface):

    def __init__(self):
        self.event_items = {}
        self.id = 0

    def save(self, event_item):
        if event_item.id is None:
            event_item.id = self.get_new_id()
        self.event_items[event_item.id] = event_item
        return event_item

    def delete(self, event_item):
        if event_item.id is None or event_item.id not in self.event_items:
            raise ValueError("error!")
        self.event_items.pop(event_item.id)

    def find_by_id(self, id):
        id = int(id)
        if id in self.event_items:
            return self.event_items[id]
        else:
            return None

    def find_all(self):
        return self.event_items

    def get_new_id(self):
        self.id = self.id + 1
        return self.id