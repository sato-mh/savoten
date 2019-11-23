from abc import ABC, abstractmethod


class UserRepositoryInterface(ABC):

    @abstractmethod
    def save(self, user):
        raise NotImplementedError

    @abstractmethod
    def delete(self, user):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def find_all(self):
        raise NotImplementedError
