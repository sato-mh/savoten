from abc import ABC, abstractmethod


class EventRepositoryInterface(ABC):

    @abstractmethod
    def save(self, event):
        raise NotImplementedError

    @abstractmethod
    def delete(self, event):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def find_by_event_id(self, event_id):
        raise NotImplementedError

    @abstractmethod
    def find_all(self):
        raise NotImplementedError
