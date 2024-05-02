import json
import logging
import pytest

from trulia.trulia_scraper import TruliaScraper
from trulia.trulia_payloadgenerator import PayloadGenerator_DetailedHouseScraper, PayloadGenerator_HouseScan

from helpers.common_helpers import *  
from trulia import constants

LOGGER = logging.getLogger(__name__)


def test_graphql_house_scan_default_query():
    houseScanner = PayloadGenerator_HouseScan()
    assert houseScanner.queryVariables == constants.TRULIA_HOUSE_SCAN_DEFAULT_QUERY_VARIABLES

def test_graphql_house_scan_properly_modifies_query():
    houseScanner = PayloadGenerator_HouseScan(
        sort='query_testing', 
        page=500,
        location = {'cities': ['abc','hello'], 'testing123': 456},
        includeOffMarket=True                        
    )
    assert houseScanner.queryVariables['searchDetails']['filters']['sort'] == 'query_testing'
    assert houseScanner.queryVariables['searchDetails']['filters']['page'] == 500
    assert houseScanner.queryVariables['searchDetails']['location'] == {'cities': ['abc','hello'], 'testing123': 456}
    assert houseScanner.queryVariables['includeOffMarket'] == True

def test_graphql_house_scan_key_not_found(caplog):
    houseScanner = PayloadGenerator_HouseScan(
        limit=400,
        incorrectKeyword='this is incorrect',
    )
    assert 'Did not find attribute "incorrectKeyword" in query options' in caplog.text
    assert houseScanner.queryVariables['searchDetails']['filters']['limit'] == 400
    assert houseScanner.queryVariables['searchDetails']['filters']['page'] == 1 #to ensure previous test cases arent affecting this one

def test_graphql_detailed_scrape_check_query_variables():
    detailedHouseScraper = PayloadGenerator_DetailedHouseScraper(['/mock_endpoint/1', '/mock/hello/world'])
    jsonPayloadAsString = json.loads(detailedHouseScraper.payload)
    expectedVariables = {"url1": "/mock_endpoint/1", "url2": "/mock/hello/world"}
    assert jsonPayloadAsString['variables'] == expectedVariables


########   NEGATIVE TEST CASES   ########

@pytest.mark.parametrize("mockUrlObject", [
    {"mockKey": "thisTestsDictionary"},
    ("thistests tuples",123,False),
    False,
    "testing123",
    12345,
    [],
])
def test_graphql_detailed_scrape_incorrect_type(mockUrlObject):
    with pytest.raises(ValueError):
        PayloadGenerator_DetailedHouseScraper(mockUrlObject)