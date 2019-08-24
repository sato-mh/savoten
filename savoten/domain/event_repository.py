from abc import ABCMeta, abstractmethod

class EventRepository(ABC):
    @abstractmethod
    def save(self, event):
        pass

    @abstractmethod
    def delete(self, event):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def find_all(self):
        pass