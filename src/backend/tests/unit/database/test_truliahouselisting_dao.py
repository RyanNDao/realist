from backend.database.dao.TruliaHouseListingDAO import TruliaHouseListingDAO
from backend.database.services.TruliaHouseListingService import TruliaHouseListingService
import pytest
from backend.database.common import constants
from backend.exceptions import CursorError
from psycopg.errors import UniqueViolation

MOCK_TABLE_NAME='mock_trulia_house_listing'

def test_get_all_listings(connectionPool):
    # rewrite
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, False)
    truliaHouseListingDAO.getAllListings(tableName=MOCK_TABLE_NAME)

def test_insert_into_table_success(mockTruliaHouseListingData, connectionPool):
    truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['only_mandatory_fields'])
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
    truliaHouseListingDAO.insertListingIntoTable(truliaHouseListingObject, tableName=MOCK_TABLE_NAME)

def test_insert_into_table_unique_key_violation(mockTruliaHouseListingData, connectionPool):
    with pytest.raises(CursorError) as exceptionObject:
        truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['base_no_normalization'])
        truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
        truliaHouseListingDAO.insertListingIntoTable(truliaHouseListingObject, tableName=MOCK_TABLE_NAME)
    assert isinstance(exceptionObject.value.cause, UniqueViolation)

def test_get_listing_by_key_object_is_returned(connectionPool):
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, False)
    returnedListing = truliaHouseListingDAO.getListingByKey(keyValue='address, zip', keyName='key', tableName=MOCK_TABLE_NAME)
    assert len(returnedListing) == len(constants.TRULIA_MAIN_TABLE_COLUMNS)
    assert isinstance(returnedListing, dict)

def test_get_listing_by_key_nothing_returned(connectionPool):
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, False)
    returnedListing = truliaHouseListingDAO.getListingByKey(keyValue='thisKeyShouldNotExist', keyName='key', tableName=MOCK_TABLE_NAME)
    assert returnedListing == None

def test_delete_listing_by_key_using_truliahouselisting_object_success(connectionPool, mockTruliaHouseListingData):
    truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['base_no_normalization'])
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
    deletedEntry = truliaHouseListingDAO.deleteListingByKeyUsingDataObject(truliaHouseListingObject, tableName=MOCK_TABLE_NAME)
    assert deletedEntry

def test_delete_listing_by_key_using_truliahouselisting_object_no_row_found(connectionPool, mockTruliaHouseListingData):
    truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['only_mandatory_fields'])
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
    deletedEntry = truliaHouseListingDAO.deleteListingByKeyUsingDataObject(truliaHouseListingObject, tableName=MOCK_TABLE_NAME)    
    assert deletedEntry == None

def test_delete_listing_by_key_success(connectionPool):
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
    deletedEntry = truliaHouseListingDAO.deleteListingByKey(key='address, zip', tableName=MOCK_TABLE_NAME)
    assert deletedEntry

def test_delete_listing_by_key_no_row_found(connectionPool):
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
    deletedEntry = truliaHouseListingDAO.deleteListingByKey(key='nosuchkey', tableName=MOCK_TABLE_NAME)    
    assert deletedEntry == None

def test_update_listing_entry_in_table_happy_path(connectionPool, mockTruliaHouseListingData):
    truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['base_no_normalization_modified'])
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
    modifiedEntry = truliaHouseListingDAO.updateListingEntryInTable(truliaHouseListingObject, tableName=MOCK_TABLE_NAME)
    assert modifiedEntry

def test_update_listing_entry_in_table_entry_properly_updates_when_null(connectionPool, mockTruliaHouseListingData):
    truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['base_no_normalization_valid_response_with_some_attributes_null_or_missing'])
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
    originalListingEntry = truliaHouseListingDAO.getListingByKey(keyValue='address, zip', keyName='key', tableName=MOCK_TABLE_NAME)
    modifiedEntry = truliaHouseListingDAO.updateListingEntryInTable(truliaHouseListingObject, tableName=MOCK_TABLE_NAME)
    assert modifiedEntry.get('asking_price') == truliaHouseListingObject.dict.get('asking_price') \
        and modifiedEntry.get('asking_price') != originalListingEntry.get('asking_price') # modified attribute with setToNullOnNonUpdate False should return as modified value
    assert modifiedEntry.get('bedrooms') == originalListingEntry.get('bedrooms') # unchanged attribute should return the same value 
    assert modifiedEntry.get('foundation') == originalListingEntry.get('foundation') # attribute with setToNullOnNonUpdate False should remain the same if attribute was not found in object
    assert modifiedEntry.get('mls_listing_id') == None # attribute with setToNullOnNonUpdate should be set to null if attribute was not found in object

def test_update_listing_entry_in_table_no_row_found(connectionPool, mockTruliaHouseListingData):
    truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['only_mandatory_fields'])
    truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
    updatedEntry = truliaHouseListingDAO.updateListingEntryInTable(truliaHouseListingObject, tableName=MOCK_TABLE_NAME)    
    assert updatedEntry == None

def test_update_listing_entry_in_table_generic_exception(connectionPool):
    with pytest.raises(Exception):
        truliaHouseListingDAO = TruliaHouseListingDAO(connectionPool, True)
        truliaHouseListingDAO.updateListingEntryInTable('this should cause an error', tableName=MOCK_TABLE_NAME)