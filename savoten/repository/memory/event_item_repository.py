from savoten import domain


class EventItemRepository(domain.EventItemRepositoryInterface):

    def __init__(self):
        self.event_items = {}
        self.id = 0

        # 本来DBテーブルに記録するevent_idとevent_itemの関係を、on_memoryの間だけ代替するdict
        # key: event_id, value: [event_item]で記載
        # on_memoryの間だけ使用する　DB仕様では不要
        self.event_id_to_event_item_map = {}

    def save(self, event_item, event_id=None):
        if event_item.id is None:
            event_item.id = self._get_new_id()
        self.event_items[event_item.id] = event_item

        # eventとの所属関係の処理
        # on_memoryからDB仕様にする時に書き換えが必要
        if event_id:
            if self.event_id_to_event_item_map.get(event_id, None):
                self.event_id_to_event_item_map[event_id].append(event_item)
            else:
                self.event_id_to_event_item_map[event_id] = [event_item]

        return event_item

    def delete(self, event_item):
        if event_item.id is None or event_item.id not in self.event_items:
            raise ValueError("error!")
        self.event_items.pop(event_item.id)

        # event_itemとの所属関係の処理
        # on_memoryからDB仕様にする時に書き換えが必要
        for event_items in self.event_id_to_event_item_map:
            if event_item in event_items:
                event_items.remove(event_item)

    def find_by_id(self, id):
        return self.event_items.get(id, None)

    def find_by_event_id(self, event_id):
        return self.event_id_to_event_item_map.get(event_id, None)

    def _get_new_id(self):
        self.id = self.id + 1
        return self.id
