
class User:

    def __init__(self, username, password):
        self._username = username
        self._password = password

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def __eq__(self, other):
        if isinstance(other, User):
            return (self._username == other._username and self._password == other._password)
