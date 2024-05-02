import logging
from trulia.trulia_payloadgenerator import PayloadGenerator_HouseScan, PayloadGenerator_DetailedHouseScraper
from trulia.trulia_scraper import TruliaScraper
from trulia.trulia_dataparser import DataParser_HouseScan, DataParser_DetailedScrape
from unittest.mock import patch, Mock
from database.services.TruliaHouseListingService import TruliaHouseListingService
from database.dao.TruliaHouseListingDAO import TruliaHouseListingDAO
import psycopg
LOGGER = logging.getLogger(__name__)


def test_end_to_end_scraping_and_parse():    
    payloadGeneratorHouseScan = PayloadGenerator_HouseScan()
    scraper = TruliaScraper(payloadGeneratorHouseScan)
    scraper.makeRequest()
    dataParserHouseScan = DataParser_HouseScan(scraper.data, scraper.payload)
    scraper.payloadGenerator = PayloadGenerator_DetailedHouseScraper(dataParserHouseScan.urls)
    scraper.makeRequest()
    dataParserDetailedScrape = DataParser_DetailedScrape(scraper.data, dataParserHouseScan.scrapedHomes)

    assert all([len(home)==32 for home in dataParserDetailedScrape.scrapedHomes.values()])