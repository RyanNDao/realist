from backend.database.common.constants import USERS_DETAIL_TABLE_NAME
from backend.database.models.User import User
from backend.database.common.DatabaseConnectionPool import DatabaseConnectionPool

class UserDAO():

    def __init__(self, connectionPool: DatabaseConnectionPool):
        self.connectionPool = connectionPool

    def getUserById(self, id: str, tableName = USERS_DETAIL_TABLE_NAME):
        with self.connectionPool.managed_connection_cursor() as cursor:
            cursor.execute(f'SELECT * FROM {tableName} WHERE id = %s', (id, ))
            userData = cursor.fetchone()
            if userData:
                pass

    def createNewUser(self, username: str, password: str, tableName = USERS_DETAIL_TABLE_NAME):
        with self.connectionPool.managed_connection_cursor() as cursor:
            cursor.execute(f'INSERT INTO {tableName}(username, password) VALUES (%s, %s)', (username, password))