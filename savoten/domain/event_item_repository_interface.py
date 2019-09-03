from abc import ABC, abstractmethod


class EventItemRepositoryInterface(ABC):
    
    @abstractmethod
    def save(self, event_item):
        raise NotImplementedError

    @abstractmethod
    def delete(self, event_item):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def find_all(self):
        raise NotImplementedError
