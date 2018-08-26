from savo.domain import Period


class Event:

    def __init__(self, name, items, id=None, start=None, end=None,
                 description=None):
        self.id = id
        self.name = name
        self.period = Period(start, end)
        self.description = description
