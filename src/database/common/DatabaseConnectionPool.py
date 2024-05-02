from psycopg_pool import ConnectionPool
from contextlib import contextmanager
import logging 

LOGGER = logging.getLogger(__name__)

class DatabaseConnectionPool:
    _instance = None

    def __new__(cls, connectionString: str = None):
        if cls._instance is None:
            if connectionString is None:
                raise ValueError('Connection string not provided for connection pool!')
            cls._instance = super(DatabaseConnectionPool, cls).__new__(cls)
            cls._instance.pool = ConnectionPool(
                conninfo=connectionString,
                min_size=2,
                max_size=6,
                open=True
            )
        return cls._instance
    
    def get_connection(self):
        return self.pool.connection()
    
    def close_pool(self):
        self.pool.close()
    
    @contextmanager
    def managed_connection_cursor(self, disableAutoCommit=False):
        try:
            with self.get_connection() as connectionInstance:
                yield connectionInstance.cursor()
                if disableAutoCommit:
                    connectionInstance.rollback()
        except Exception as e:
            LOGGER.error(f"Database error: {e}")
            raise Exception(e)
        finally:
            pass