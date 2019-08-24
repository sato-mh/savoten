from abc import ABCMeta, abstractmethod

class EventRepository(ABC):
    @abstractmethod
    def save(self, event):
        pass

    @abstractmethod
    def delete(self, event):
        pass

    @abstractmethod
    def findById(self, id):
        pass

    @abstractmethod
    def findAll(self):
        pass