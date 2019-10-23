from savoten.domain import UserRepositoryInterface


class UserRepository(UserRepositoryInterface):

    def __init__(self):
        self.users = {}
        self.id = 0

    def save(self, user):
        if user.id is None:
            user.id = self._get_new_id()
        self.users[user.id] = user
        return user

    def delete(self, user):
        if user.id is None or user.id not in self.users:
            raise ValueError("error!")
        self.users.pop(user.id)

    def find_by_id(self, id):
        return self.users.get(id, None)

    def find_all(self):
        return self.users.values()

    def _get_new_id(self):
        self.id = self.id + 1
        return self.id
