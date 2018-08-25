
class User:

    def __init__(self, name, email, permission,
            created_at, updated_at, deleted_at, id=None):
        self.id = id
        self.name = name
        self.permission = permission
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
