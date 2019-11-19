from .event_item import EventItem
from .period import Period


class Event:

    def __init__(self,
                 name,
                 items,
                 period,
                 id=None,
                 description=None,
                 anonymous=False,
                 created_at=None,
                 updated_at=None,
                 deleted_at=None):
        self.id = id
        self.name = name
        self.items = items
        self.period = period
        self.description = description
        self.anonymous = anonymous
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        if not (isinstance(items, list) and  # noqa: W504
                all([isinstance(item, EventItem) for item in items])):
            raise TypeError('items is required List[EventItem]. not {}.'.format(
                type(items)))
        self._items = items

    @property
    def period(self):
        return self._period

    @period.setter
    def period(self, period):
        if not isinstance(period, Period):
            raise TypeError('period is required {}. not {}.'.format(
                Period, type(period)))
        self._period = period

    def is_within(self):
        return self.period.is_within()
