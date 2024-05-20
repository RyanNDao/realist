import logging
from backend.scrapers.trulia.trulia_payloadgenerator import PayloadGenerator_HouseScan, PayloadGenerator_DetailedHouseScraper
from backend.scrapers.trulia.trulia_scraper import TruliaScraper
from backend.scrapers.trulia.trulia_dataparser import DataParser_HouseScan, DataParser_DetailedScrape
from unittest.mock import patch, Mock
from backend.database.services.TruliaHouseListingService import TruliaHouseListingService
from backend.database.dao.TruliaHouseListingDAO import TruliaHouseListingDAO

LOGGER = logging.getLogger(__name__)


def test_end_to_end_scraping_and_parse():
    # the end to end flow is a little confusing
    # TODO: refactor this so that its intuitive
    payloadGeneratorHouseScan = PayloadGenerator_HouseScan()
    scraper = TruliaScraper(payloadGeneratorHouseScan)
    scraper.makeRequest()
    dataParserHouseScan = DataParser_HouseScan(scraper.data, scraper.payload)
    scraper.payloadGenerator = PayloadGenerator_DetailedHouseScraper(dataParserHouseScan.urls)
    scraper.makeRequest()
    dataParserDetailedScrape = DataParser_DetailedScrape(scraper.data, dataParserHouseScan.scrapedHomes)

    assert all([len(home)==32 for home in dataParserDetailedScrape.scrapedHomes.values()])