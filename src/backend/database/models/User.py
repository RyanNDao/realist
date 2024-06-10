

from flask_login import UserMixin


class User(UserMixin):
    
    def __init__(self, id: str, username: str, passwordHash: str):
        self.id = id
        self.username = username
        self.passwordHash = passwordHash

    