from contextlib import contextmanager
import uuid
from backend.database.common.DatabaseConnectionPool import DatabaseConnectionPool
from backend.database.common.constants import TRULIA_MAIN_TABLE_NAME, TRULIA_MAIN_TABLE_VALUES, TRULIA_MAIN_TABLE_COLUMNS
import logging
from backend.database.models.TruliaHouseListing import TruliaHouseListing
from backend.helpers.database_helpers import build_dynamic_update_query_template
from backend.server.utils.CommonLogger import CommonLogger



class TruliaHouseListingDAO():

    def __init__(self, connectionPool: DatabaseConnectionPool, disableAutoCommit=False):
        self.connectionPool = connectionPool
        self.disableAutoCommit = disableAutoCommit

    #TODO: Combine all these three functions 
    def getAllListings(self, tableName=TRULIA_MAIN_TABLE_NAME) -> list:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            cursor.execute(f"SELECT * FROM {tableName} WHERE listing_status = 'For Sale'")
            rows = cursor.fetchall()
            CommonLogger.LOGGER.info(f'getAllListings returned {len(rows)} total results')
            return rows
        
    def getAllRentals(self, tableName=TRULIA_MAIN_TABLE_NAME) -> list:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            cursor.execute(f"SELECT * FROM {tableName} WHERE listing_status = 'For Rent'")
            rows = cursor.fetchall()
            CommonLogger.LOGGER.info(f'getAllRentals returned {len(rows)} total results')
            return rows
        
    def getAllSold(self, tableName=TRULIA_MAIN_TABLE_NAME) -> list:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            cursor.execute(f"SELECT * FROM {tableName} WHERE listing_status = 'Sold'")
            rows = cursor.fetchall()
            CommonLogger.LOGGER.info(f'getAllSold returned {len(rows)} total results')
            return rows
        
    def insertListingIntoTable(self, truliaHouseListing: TruliaHouseListing, columns=TRULIA_MAIN_TABLE_VALUES, tableName=TRULIA_MAIN_TABLE_NAME) -> None:
        # this shouldn't be used, even with one entry. Use the insert multiple instead.
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            if not isinstance(truliaHouseListing, TruliaHouseListing):
                raise AttributeError(f'truliaHouseListing is of type {type(truliaHouseListing)}, when it should be a TruliaHouseListing type!')
            cursor.execute(f'INSERT INTO {tableName} {columns};', truliaHouseListing.dict)
            # CommonLogger.LOGGER.info(f'Inserted {cursor.statusmessage.split(" ")[-1]} house listing(s) in {tableName}!')

    def insertMultipleListingsIntoTable(self, truliaHouseListingList: list[TruliaHouseListing], columns=TRULIA_MAIN_TABLE_VALUES, tableName=TRULIA_MAIN_TABLE_NAME) -> None:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            if not all([isinstance(entry, TruliaHouseListing) for entry in truliaHouseListingList]):
                raise AttributeError(f'All entries must be of TruliaHouseListing type when trying to insert multiple listings into DB table {tableName}')
            tempTable = f'{tableName}_temp_{uuid.uuid4().hex}'
            try:
                cursor.execute(f"CREATE TABLE {tempTable} (LIKE {tableName} INCLUDING ALL)") # create empty temp table
                cursor.executemany(f'INSERT INTO {tempTable} {columns};', [entry.dict for entry in truliaHouseListingList])
                cursor.execute(f'INSERT INTO {tableName} {columns.split(" VALUES ")[0]} SELECT {columns.split(" VALUES ")[0][1:-1]} FROM {tempTable} ON CONFLICT DO NOTHING')
                successfulEntries = cursor.rowcount
                cursor.execute(f'SELECT * FROM {tempTable} EXCEPT SELECT * FROM {tableName}') # get differences in tables
                failedEntries = cursor.fetchall()
                for entry in failedEntries:
                    CommonLogger.LOGGER.warning(f'Listing {entry} was not inserted due to a conflict.')
                CommonLogger.LOGGER.warning(f'Total inserted rows: {successfulEntries}') 
            except Exception as e:
                cursor.execute("ROLLBACK;")
                CommonLogger.LOGGER.error(f'An error has occurred while inserting multiple listings into {tableName}: {e}')
            finally:
                cursor.execute(f"DROP TABLE IF EXISTS {tempTable};")

    def getListingByKey(self, keyValue: str, keyName='key', tableName=TRULIA_MAIN_TABLE_NAME) -> dict:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            cursor.execute(f'SELECT * FROM {tableName} WHERE {keyName} = %s', (keyValue, ))
            return cursor.fetchone()
    
    def deleteListingByKey(self, key: str, tableName=TRULIA_MAIN_TABLE_NAME) -> None:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            cursor.execute(f'DELETE FROM {tableName} WHERE key = %s RETURNING *', (key,))
            deletedListing = cursor.fetchone()
            if deletedListing is None:
                CommonLogger.LOGGER.warning(f'No row with the key "{key}" was found while trying to delete!')
            else:
                CommonLogger.LOGGER.info(f'Deleted row from {tableName} with the key: "{key}"')
            return deletedListing

    def deleteListingByKeyUsingDataObject(self, truliaHouseListing: TruliaHouseListing, tableName=TRULIA_MAIN_TABLE_NAME) -> None:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            key = truliaHouseListing.key
            cursor.execute(f'DELETE FROM {tableName} WHERE key = %s RETURNING *', (key,))
            deletedListing = cursor.fetchone()
            if deletedListing is None:
                CommonLogger.LOGGER.warning(f'No row with the key "{key}" was found while trying to delete!')
            else:
                CommonLogger.LOGGER.info(f'Deleted row from {tableName} with the key: "{key}"')
            return deletedListing

    def updateListingEntryInTable(self, truliaHouseListing: TruliaHouseListing, tableName=TRULIA_MAIN_TABLE_NAME, keyName = 'key'):
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            setQueryTemplate = build_dynamic_update_query_template(TRULIA_MAIN_TABLE_COLUMNS, keyName=keyName)
            setQueryTemplate = setQueryTemplate.format(tableName=tableName, keyName=keyName)
            cursor.execute(setQueryTemplate, truliaHouseListing.dict)
            updatedListing = cursor.fetchone()
            if updatedListing is None:
                CommonLogger.LOGGER.warning(f'No row with the key "{keyName}" was found while trying to delete!')
            else:
                CommonLogger.LOGGER.info(f'Updated row from {tableName} with the key: "{updatedListing.get("keyName")}"')
            return updatedListing
        
    def updateMultipleListingsInTable(self, truliaHouseListingList: list[TruliaHouseListing], tableName=TRULIA_MAIN_TABLE_NAME, keyName = 'key'):
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            if not all([isinstance(entry, TruliaHouseListing) for entry in truliaHouseListingList]):
                raise AttributeError(f'All entries must be of TruliaHouseListing type when trying to update multiple listings into DB table {tableName}')
            setQueryTemplate = build_dynamic_update_query_template(TRULIA_MAIN_TABLE_COLUMNS, keyName=keyName)
            setQueryTemplate = setQueryTemplate.format(tableName=tableName, keyName=keyName)
            cursor.executemany(setQueryTemplate, [entry.dict for entry in truliaHouseListingList])
            CommonLogger.LOGGER.warning(f'Total updated rows: {cursor.rowcount}')