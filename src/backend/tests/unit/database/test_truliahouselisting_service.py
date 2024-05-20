from backend.database.models.TruliaHouseListing import TruliaHouseListing
from backend.database.services.TruliaHouseListingService import TruliaHouseListingService
from datetime import datetime



def test_trulia_house_listing_object_creation(mockTruliaHouseListingData):
    truliaHouseListingObject = TruliaHouseListingService.createTruliaHouseListingDataObject(mockTruliaHouseListingData['base_no_normalization'])
    assert isinstance(truliaHouseListingObject, TruliaHouseListing)

def test_normalize_home_data(mockTruliaHouseListingData):
    truliaHouseListingObject = TruliaHouseListingService.normalizehomeDictData(mockTruliaHouseListingData['base_no_normalization'])
    assert truliaHouseListingObject['key'] == 'address, zip'
    assert truliaHouseListingObject['floor_sqft'] == 123
    assert truliaHouseListingObject['lot_sqft'] == 456
    assert truliaHouseListingObject['date_listed_or_sold'] == datetime(2022, 1, 1)
    assert truliaHouseListingObject['year_built'] == 2000
    assert truliaHouseListingObject['year_renovated'] == 2010
    assert TruliaHouseListing(**truliaHouseListingObject) == TruliaHouseListing(**mockTruliaHouseListingData['base_normalized'])