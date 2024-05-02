import psycopg
from database.dao.TruliaHouseListingDAO import TruliaHouseListingDAO
from database.services.TruliaHouseListingService import TruliaHouseListingService




def test_get_all_listings(connectionPool):
    # rewrite
    with connectionPool.managed_connection_cursor() as cursor:
        truliaHouseListingDAO = TruliaHouseListingDAO(cursor)
        truliaHouseListingDAO.getAllListings()

def test_insert_into_table(mockTruliaHouseListingData, connectionPool):
    truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['base_no_normalization'])
    with connectionPool.managed_connection_cursor(disableAutoCommit=True) as cursor:
        truliaHouseListingDAO = TruliaHouseListingDAO(cursor)
        truliaHouseListingDAO.insertListingIntoTable(truliaHouseListingObject)
