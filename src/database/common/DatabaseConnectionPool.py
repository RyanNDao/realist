from psycopg_pool import ConnectionPool
from contextlib import contextmanager
from exceptions import CursorError
import psycopg
import logging 
from psycopg import Error, errors

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
                yield connectionInstance.cursor(row_factory=psycopg.rows.dict_row)
                if disableAutoCommit:
                    LOGGER.info('Autocommit was disabled so transaction was rolled back!')
                    connectionInstance.rollback()
        except psycopg.Error as psycopgError:
            LOGGER.error(f"A PostgreSQL error occurred when using a managed cursor: {psycopgError}")
            raise CursorError(psycopgError, cause=psycopgError, type=errors.lookup(psycopgError.sqlstate))
        except Exception as e:
            LOGGER.error(f"The error type <{type(e).__name__}> occurred when using a managed cursor: {e}")
            raise Exception(e)
        finally:
            pass