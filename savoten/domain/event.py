from savo.domain import EventItem, Period


class Event:

    def __init__(self, name, items, id=None, start=None, end=None,
                 description=None, anonymous=False,
                 created_at=None, updated_at=None, deleted_at=None):
        self.id = id
        self.name = name
        self.items = items
        self.period = Period(start, end)
        self.description = description
        self.anonymous = anonymous
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @property
    def items(self):
        return self.items

    @items.setter
    def items(self, items):
        if not (isinstance(items, list)
                and all([isinstance(item, EventItem) for item in items])):
            raise TypeError('items is required List[EventItem]. not {}.'
                            .format(list, type(items)))

    def is_within(self):
        return self.period.is_within()
