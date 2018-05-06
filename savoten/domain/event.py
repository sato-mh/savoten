import datetime


class Event:

    def __init__(self, name, items, period=None, description=None, id=None):
        self.id = id
        self.name = name
        self.items = items
        self.period = period
        self.description = description


class Period:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if not self._is_datetime(start):
            raise TypeError('start is required {}. not {}.'
                            .format(datetime.datetime, type(start)))
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if not self._is_datetime(end):
            raise TypeError('end is required {}. not {}.'
                            .format(datetime.datetime, type(end)))
        self._end = end

    @staticmethod
    def _is_datetime(arg):
        return isinstance(arg, datetime.date)

    def is_within(self):
        now = datetime.datetime.now()
        return self.start < now < self.end
