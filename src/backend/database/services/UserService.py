from backend.database.dao.UserDAO import UserDAO

class UserService():

    def __init__(self, userDAO: UserDAO):
        self._userDAO = userDAO

    def createUser(self, username: str, passwordHash: bytes):
        self._userDAO.createNewUser(username, password=passwordHash)