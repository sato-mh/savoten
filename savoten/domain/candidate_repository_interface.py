from abc import ABC, abstractmethod


class CandidateRepositoryInterface(ABC):

    @abstractmethod
    def save(self, candidate, event_item_id=None):
        raise NotImplementedError

    @abstractmethod
    def delete(self, candidate):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def find_by_event_item_id(self, event_item_id):
        raise NotImplementedError

    @abstractmethod
    def find_all(self):
        raise NotImplementedError
