from psycopg_pool import ConnectionPool
from contextlib import contextmanager
from backend.exceptions import CursorError
import psycopg
import logging 
from psycopg import Error, errors

from backend.server.utils.CommonLogger import CommonLogger



class DatabaseConnectionPool:

    def __init__(self, connectionString: str = None):
        if connectionString is None:
            raise ValueError('Connection string not provided for connection pool!')
        self.pool = ConnectionPool(
            conninfo=connectionString,
            min_size=2,
            max_size=6,
            check=ConnectionPool.check_connection,
            open=True
        )
    
    def get_connection(self):
        return self.pool.connection()
    
    def close_pool(self):
        self.pool.close()

    def get_pool_stats(self):
        return self.pool.get_stats()
    
    @contextmanager
    def managed_connection_cursor(self, disableAutoCommit=False):
        try:
            with self.get_connection() as connectionInstance:
                yield connectionInstance.cursor(row_factory=psycopg.rows.dict_row)
                if disableAutoCommit:
                    CommonLogger.LOGGER.warning('Autocommit was disabled so transaction was rolled back!')
                    connectionInstance.rollback()
        except psycopg.Error as psycopgError:
            CommonLogger.LOGGER.error(f"A PostgreSQL error occurred when using a managed cursor: {psycopgError}")
            raise CursorError(psycopgError, cause=psycopgError, type=errors.lookup(psycopgError.sqlstate) if psycopgError.sqlstate else None)
        except Exception as e:
            CommonLogger.LOGGER.error(f"The error type <{type(e).__name__}> occurred when using a managed cursor: {e}")
            raise Exception(e)
        finally:
            pass