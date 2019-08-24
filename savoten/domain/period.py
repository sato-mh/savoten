from datetime import date, datetime


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
            raise TypeError('start is required {}. not {}.'.format(
                datetime, type(start)))
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if not self._is_datetime(end):
            raise TypeError('end is required {}. not {}.'.format(
                datetime, type(end)))
        self._end = end

    @staticmethod
    def _is_datetime(arg):
        return isinstance(arg, date)

    def is_within(self):
        now = datetime.now()
        return self.start < now < self.end
