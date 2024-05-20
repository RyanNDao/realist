import pytest
from database.models.TruliaHouseListing import TruliaHouseListing
from database.models.ModelAttribute import ModelAttribute
from database.common import constants

@pytest.mark.parametrize("testName", [
    ("base_normalized"),
    ("optional_fields_null"),
    ("only_mandatory_fields")
])
def test_truliahouselisting_dict_returns_correct_dict(mockTruliaHouseListingData, testName):
    testData = mockTruliaHouseListingData[testName]
    truliaHouseListingObject = TruliaHouseListing(**testData)
    assert len(truliaHouseListingObject.dict) == len(constants.TRULIA_MAIN_TABLE_COLUMNS)

def test_truliahouselisting_empty_attributes_are_none(mockTruliaHouseListingData):
    truliaHouseListingObject = TruliaHouseListing(**mockTruliaHouseListingData['only_mandatory_fields'])
    assert not any(isinstance(value, ModelAttribute) for value in truliaHouseListingObject.dict.values())
    assert any(value==None for value in truliaHouseListingObject.dict.values())

@pytest.mark.parametrize("testName", [
    ("some_null_mandatory_fields"),
    ("some_missing_mandatory_fields"),
    ("wrong_optional_types"),
    ("wrong_mandatory_types")
])
def test_truliahouselisting_validation_errors(mockTruliaHouseListingData, testName):
    testData = mockTruliaHouseListingData[testName]
    with pytest.raises(TypeError):
        TruliaHouseListing(**testData)

def test_truliahouselisting_equality(mockTruliaHouseListingData):
    mockObjectOne = TruliaHouseListing(**mockTruliaHouseListingData['base_normalized'])
    mockObjectTwo = TruliaHouseListing(**mockTruliaHouseListingData['base_normalized'])
    assert mockObjectOne == mockObjectTwo


def test_truliahouselisting_equality_negative(mockTruliaHouseListingData):
    mockObjectOne = TruliaHouseListing(**mockTruliaHouseListingData['base_normalized'])
    mockObjectTwo = TruliaHouseListing(**mockTruliaHouseListingData['only_mandatory_fields'])
    assert mockObjectOne != mockObjectTwo