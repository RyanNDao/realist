import pytest
import json
import os
from dotenv import load_dotenv
from unittest.mock import Mock
from trulia.trulia_scraper import TruliaScraper
from trulia.trulia_payloadgenerator import PayloadGenerator_HouseScan, PayloadGenerator_DetailedHouseScraper
from database.models.TruliaHouseListing import TruliaHouseListing
from .data.fixtures_data import *
from database.common.DatabaseConnectionPool import DatabaseConnectionPool

pytest.testDirectory = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

def pytest_configure(config):
    loadAllJsonData()

def loadAllJsonData():
    jsonDirectory = os.path.join(pytest.testDirectory, 'data')
    pytest.JSON_DATA = {}
    for filename in os.listdir(jsonDirectory):
        if filename.endswith('.json'):
            file_path = os.path.join(jsonDirectory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                key = os.path.splitext(filename)[0]
                pytest.JSON_DATA[key] = json.load(file)

@pytest.fixture(scope="session")
def connectionPool():
    pool = DatabaseConnectionPool(connectionString=os.getenv('CONNECTION_STRING'))
    yield pool
    pool.close_pool()

@pytest.fixture(autouse=True)
def mockTruliaApiCall(mocker):
    def mockResponseBasedOnPayloadGeneratorObject(instance):
        mockResponseReturnObject = Mock()
        if isinstance(instance.payloadGenerator, PayloadGenerator_HouseScan):
            mockResponseReturnObject.status_code = 200
            mockResponseReturnObject.text = pytest.JSON_DATA['mocked_trulia_house_scan_response_default']
        elif isinstance(instance.payloadGenerator, PayloadGenerator_DetailedHouseScraper):
            mockResponseReturnObject.status_code = 200
            mockResponseReturnObject.text = pytest.JSON_DATA['mocked_trulia_detailed_scrape_response_default']
        else:
            mockResponseReturnObject.status_code = 400
            mockResponseReturnObject.text = 'instance payloadGenerator attribute is not a PayloadGenerator object'
        return mockResponseReturnObject
    mocker.patch.object(TruliaScraper, 'returnResponse', mockResponseBasedOnPayloadGeneratorObject)

@pytest.fixture
def mockTruliaHouseListingData():
    return truliaHouseListingTestDicts