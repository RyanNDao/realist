from contextlib import contextmanager
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
            CommonLogger.LOGGER.info(f'getAllListings returned {len(rows)} total results')
            return rows
        
    def insertListingIntoTable(self, truliaHouseListing: TruliaHouseListing, columns=TRULIA_MAIN_TABLE_VALUES, tableName=TRULIA_MAIN_TABLE_NAME) -> None:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            if not isinstance(truliaHouseListing, TruliaHouseListing):
                raise AttributeError(f'truliaHouseListing is of type {type(truliaHouseListing)}, when it should be a TruliaHouseListing type!')
            cursor.execute(f'INSERT INTO {tableName} {columns};', truliaHouseListing.dict)
            # CommonLogger.LOGGER.info(f'Inserted {cursor.statusmessage.split(" ")[-1]} house listing(s) in {tableName}!')

    def insertMultipleListingsIntoTable(self, truliaHouseListingList: list[TruliaHouseListing], columns=TRULIA_MAIN_TABLE_VALUES, tableName=TRULIA_MAIN_TABLE_NAME) -> None:
        with self.connectionPool.managed_connection_cursor(self.disableAutoCommit) as cursor:
            if not all([isinstance(entry, TruliaHouseListing) for entry in truliaHouseListingList]):
                raise AttributeError(f'All entries must be of TruliaHouseListing type when trying to insert multiple listings into DB table {tableName}')
            cursor.executemany(f'INSERT INTO {tableName} {columns};', [entry.dict for entry in truliaHouseListingList])
            CommonLogger.LOGGER.warning(f'Total inserted rows: {cursor.rowcount}')

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