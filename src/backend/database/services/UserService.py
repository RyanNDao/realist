from backend.database.dao.UserDAO import UserDAO
import bcrypt
class UserService():

    def __init__(self, userDAO: UserDAO):
        self._userDAO = userDAO

    def createUser(self, username: str, passwordHash: bytes):
        self._userDAO.createNewUser(username, password=passwordHash)

    def authenticate(self, username: str, password: bytes):
        user = self._userDAO.getUserByUsername(username)
        if not user:
            return None
        return user if bcrypt.checkpw(password,user.get('password', '').encode('utf-8')) else None
