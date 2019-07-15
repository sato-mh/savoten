from abc import ABCMeta, abstractmethod

class EventRepository(metaclass=ABCMeta):
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