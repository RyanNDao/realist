from trulia.trulia_dataparser import HouseScan_DataParser, DetailedScrape_DataParser, DataParser
import pytest
from unittest.mock import Mock, patch


def test_trulia_house_scan_data_parser_default(caplog):
    houseScanDataParser = HouseScan_DataParser(
        pytest.JSON_DATA['mocked_trulia_house_scan_response_default'],
        pytest.JSON_DATA['expected_house_scan_default_payload']
    )
    assert 'Liberty Plaza View Plan in North Liberty Triangle was not added due to non-specific asking price' in caplog.text
    assert len(houseScanDataParser.scrapedHomes) == 24
    assert len(houseScanDataParser.urls) == 24
    
def test_trulia_house_scan_check_home_data():
    houseScanDataParser = HouseScan_DataParser(
        pytest.JSON_DATA['mocked_trulia_house_scan_response_default'],
        pytest.JSON_DATA['expected_house_scan_default_payload']
    )
    homeData = houseScanDataParser.scrapedHomes[0]
    assert homeData['location']
    assert homeData['address']
    assert homeData['asking_price']
    assert homeData['url']
    assert homeData['trulia_url']
    assert homeData['city']
    assert homeData['state']
    assert homeData['zip']
    assert homeData['floor_sqft']
    assert homeData['lot_size'] == None
    assert homeData['bedrooms'] and type(homeData['bedrooms']) == str
    assert homeData['bathrooms'] and type(homeData['bathrooms']) == str
    assert homeData['trulia_listing_id']
    assert homeData['date_listed_or_sold']
    assert homeData['listing_status']
    assert homeData['neighborhood']
    assert homeData['property_type']
    assert homeData['parking']
    assert homeData['year_built']
    assert len(homeData) == 19


def test_trulia_detailed_scrape_default():
    DetailedScrape_DataParser
    





@pytest.mark.parametrize("path,default,expected", [
    (['abc', 'def'], None, 'hello'),
    (['abc', 'xyz'], None, 'world'),
    (['abc', 'nokey'], 'nokeyfound', 'nokeyfound'),
    (['abc', 'asd'], 'default', {'def': 'goodbye'}),
    (['abc', 'asd', 'def'], 'default', 'goodbye'),
    (['hello'], 'this is default', 'this is default'),
    (['abcdef'], None, 'def'),
])
def test_getAttribute_with_default_parse(path, default, expected):
    mockObj = {
        "abc": {
            "def": "hello",
            "xyz": "world",
            "asd": {
                "def": "goodbye"
            }
        },
        "hello": None,
        "abcdef": "def"
    }
    assert DataParser.getAttribute(mockObj, path, default, parserFunction=DataParser.defaultParse) == expected

def test_getAttribute_error_handling(caplog):
    mockFunction = Mock()
    mockFunction.__name__ = 'mockFunction'
    mockFunction.side_effect = RuntimeError('Mocked error')
    DataParser.getAttribute({}, [], 'default_value', parserFunction=mockFunction) == 'default_value'
    mockFunction.assert_called_once()
    assert 'A(n) RuntimeError has occurred while extracting home data: Mocked error' in caplog.text

def test_getListingStatus_custom_default():
    mockObj = {'currentStatus': {}}
    assert DataParser.getAttribute(mockObj, None, default='test', parserFunction=HouseScan_DataParser.getListingStatus) == 'test'

@pytest.mark.parametrize("status_key, expected_status", [
    ('isRecentlySold', 'Sold'),
    ('isRecentlyRented', 'Rented'),
    ('isActiveForRent', 'For Rent'),
    ('isActiveForSale', 'For Sale'),
    ('isOffMarket', 'Off Market'),
    ('isForeclosure', 'Foreclosure'),
])
def test_getListingStatus_with_statuses(status_key, expected_status):
    mockObj = {'currentStatus': {status_key: True, 'hello': False}}
    assert DataParser.getAttribute(mockObj, None, None, parserFunction=HouseScan_DataParser.getListingStatus) == expected_status

@pytest.mark.parametrize("trackingList,key,default,expected", [
    ([{'key': 'testKey', 'value': 'testValue'}], 'testKey', None, 'testValue'),
    ([{'key': 'anotherKey', 'value': 'anotherValue'}], 'testKey', 'defaultValue', 'defaultValue'),
    ([{'key': 'testKey', 'value': 'firstValue'}, {'key': 'testKey', 'value': 'secondValue'}], 'testKey', 'multipleFound', 'multipleFound'),
])
def test_parseTrackingList(trackingList, key, default, expected):
    assert DataParser.getAttribute(trackingList, key, default, parserFunction=HouseScan_DataParser.parseTrackingList) == expected

@pytest.mark.parametrize("trackingList,keyword,default,expected", [
    ([{'key': 'item', 'value': 'keyword:expectedValue;'}], 'keyword', None, 'expectedValue'),
    ([{'key': 'item', 'value': 'substring:thistestssubstring;'}], 'string', None, None),
    ([{'key': 'item', 'value': 'anotherKeyword:anotherValue;'}], 'keyword', 'notFound', 'notFound'),
    ([{'key': 'item', 'value': '|keyword:this_also_tests_symbols;'}, {'key': 'item', 'value': ':keyword:secondValue;'}], 'keyword', 'multipleFound', 'multipleFound'),
    ([{'key': 'item', 'value': 'no match'}], 'keyword', 'noMatch', 'noMatch'),
])
def test_parseMiscItemsInTrackingList(trackingList, keyword, default, expected):
    assert DataParser.getAttribute(trackingList, keyword, default, parserFunction=HouseScan_DataParser.parseMiscItemsInTrackingList) == expected

@pytest.mark.parametrize("home,path,default,expected", [
    ({"bathrooms": {"summaryBathrooms": "!wow2ba"}}, ['bathrooms', 'summaryBathrooms'], None, '2'),
    ({"bedrooms": {"summaryBedrooms": "hello3studio"}}, ['bedrooms', 'summaryBedrooms'], None, '3'),
    ({"bathrooms": {"summaryBathrooms": "studio"}}, ['bathrooms', 'summaryBathrooms'], None, 'studio'),
    ({}, ['bathrooms', 'summaryBathrooms'], 'default', 'default'),
    ({"bedrooms": {}}, ['bedrooms', 'summaryBedrooms'], 'testing', 'testing'),
])
def test_getBathroomsBedrooms(home, path, default, expected):
    assert DataParser.getAttribute(home, path, default, parserFunction=HouseScan_DataParser.getBathroomsBedrooms) == expected

@pytest.mark.parametrize("home,searchType,default,expected", [
    ({"activeListing": {"dateListed": "2022-01-02T12:34:56"}}, 'FOR_SALE', None, '2022-01-02'),
    ({"fullTags": [{}, {"formattedName": "Feb 2, 2022"}]}, 'SOLD', None, '2022-02-02'),
    ({}, 'FOR_RENT', 'testdefault', 'testdefault')
])
def test_getDateListedOrSold(home, searchType, default, expected):
    assert DataParser.getAttribute(home, None, default, parserFunction=HouseScan_DataParser.getDateListedOrSold, searchType=searchType) == expected