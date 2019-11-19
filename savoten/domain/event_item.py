from .candidate import Candidate


class EventItem:

    def __init__(self,
                 name,
                 candidates,
                 description=None,
                 seats=1,
                 max_choice=1,
                 min_choice=1,
                 id=None):
        self.id = id
        self.name = name
        self.candidates = candidates
        self.description = description
        self.seats = seats
        self.max_choice = max_choice
        self.min_choice = min_choice

    @property
    def candidates(self):
        return self._candidates

    @candidates.setter
    def candidates(self, candidates):
        if not (isinstance(candidates, list) and  # noqa: W504
                all([isinstance(c, Candidate) for c in candidates])):
            raise TypeError('items is required List[Candidate]. not {}.'.format(
                type(candidates)))
        self._candidates = candidates
