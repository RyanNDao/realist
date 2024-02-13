import logging
import pytest
from trulia.trulia_payloadgenerator import PayloadGenerator_HouseScan, PayloadGenerator_DetailedHouseScraper
from trulia.trulia_scraper import TruliaScraper
import json
from unittest.mock import patch, Mock

LOGGER = logging.getLogger(__name__)

def test_trulia_scraper_house_scan_default_payload():
    scraper = TruliaScraper(PayloadGenerator_HouseScan())
    assert json.loads(scraper.payload) == pytest.JSON_DATA['expected_house_scan_default_payload']
    
def test_trulia_scraper_house_scan_modified_payload():
    scraper = TruliaScraper(PayloadGenerator_HouseScan(
        location = {
            "zips": [
                "19132"
            ]
        },
        ascending=True,
        limit=100,
        includeOffMarket=True
    ))
    assert json.loads(scraper.payload) == pytest.JSON_DATA['expected_house_scan_modified_variables_payload']

def test_trulia_scraper_detailed_scrape():
    scraper = TruliaScraper(PayloadGenerator_DetailedHouseScraper([
        'endpoint/to/scrape1',
        'endpoint/1/',
        'testing/1/mock/3/'
    ]))
    assert json.loads(scraper.payload) == pytest.JSON_DATA['expected_detailed_scrape_payload']

@patch('trulia.trulia_scraper.requests.request')
def test_trulia_scraper_house_scan_make_request(mockResponse):
    mockResponseReturn = Mock()
    mockResponseReturn.status_code = 200
    mockResponseReturn.text = pytest.JSON_DATA['mocked_trulia_house_scan_response_default']
    mockResponse.return_value = mockResponseReturn
    scraper = TruliaScraper(PayloadGenerator_HouseScan())
    assert scraper.data == None
    scraper.makeRequest()
    assert scraper.data == pytest.JSON_DATA['mocked_trulia_house_scan_response_default']

@patch('trulia.trulia_scraper.requests.request')
def test_trulia_scraper_detailed_scrape_make_request(mockResponse):
    mockResponseReturn = Mock()
    mockResponseReturn.status_code = 200
    mockResponseReturn.text = pytest.JSON_DATA['mocked_trulia_detailed_scrape_response_simple']
    mockResponse.return_value = mockResponseReturn
    scraper = TruliaScraper(PayloadGenerator_DetailedHouseScraper([
        "/home/230-montrose-st-philadelphia-pa-19147-10177108",
        "/home/200-head-house-ct-philadelphia-pa-19147-10182414"
    ]))
    assert scraper.data == None
    scraper.makeRequest()
    assert scraper.data == pytest.JSON_DATA['mocked_trulia_detailed_scrape_response_simple']

########   NEGATIVE TEST CASES   ########

def test_trulia_scraper_invalid_data_type():
    scraper1 = TruliaScraper(PayloadGenerator_HouseScan())
    scraper2 = TruliaScraper(PayloadGenerator_DetailedHouseScraper(['test']))
    with pytest.raises(AttributeError):
        scraper1.data = 1234
    with pytest.raises(AttributeError):
        scraper2.data = ['this','should','fail']

@pytest.mark.parametrize("mockScraperTypeObject", [
    {"mockKey": "thisTestsDictionary"},
    ("thistests tuples",123,False),
    False,
    "testing123",
    12345,
    [],
])
def test_trulia_scraper_invalid_scraper_type(mockScraperTypeObject):
    with pytest.raises(AttributeError):
        TruliaScraper(mockScraperTypeObject)
