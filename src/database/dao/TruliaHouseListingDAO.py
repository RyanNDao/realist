from contextlib import contextmanager
from database.common import constants
import logging
from database.models.TruliaHouseListing import TruliaHouseListing

LOGGER = logging.getLogger(__name__)

class TruliaHouseListingDAO():

    def __init__(self, cursor):
        self.cursor = cursor

    def getAllListings(self, tableName=constants.TRULIA_MAIN_TABLE_NAME):
        self.cursor.execute(f'SELECT * FROM {tableName}')
        rows = self.cursor.fetchall()
        LOGGER.info(f'getAllListings returned {len(rows)} total results')
        return rows
        
    def insertListingIntoTable(self, truliaHouseListing: TruliaHouseListing, columns= constants.TRULIA_MAIN_TABLE_VALUES, tableName=constants.TRULIA_MAIN_TABLE_NAME):
        if not isinstance(truliaHouseListing, TruliaHouseListing):
            raise AttributeError(f'truliaHouseListing is of type {type(truliaHouseListing)}, when it should be a TruliaHouseListing type!')
        self.cursor.execute(f'INSERT INTO {tableName} {columns};', truliaHouseListing.dict)