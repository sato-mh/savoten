from .user import User


class Candidate:

    def __init__(self, user, description=None, id=None):
        self.id = id
        self.user = user
        self.description = description

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if not isinstance(user, User):
            raise TypeError('items is required {}. not {}.'.format(
                User, type(user)))
        self._user = user
