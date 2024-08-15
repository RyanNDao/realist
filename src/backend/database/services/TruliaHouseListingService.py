from backend.database.models.TruliaHouseListing import TruliaHouseListing
from backend.database.dao.TruliaHouseListingDAO import TruliaHouseListingDAO
import copy
import re
from datetime import datetime
from backend.helpers.common_helpers import safeParseInt
from backend.scrapers.trulia.trulia_dataparser import DataParser_DetailedScrape, DataParser_HouseScan
from backend.scrapers.trulia.trulia_payloadgenerator import PayloadGenerator_DetailedHouseScraper, PayloadGenerator_HouseScan
from backend.scrapers.trulia.trulia_scraper import TruliaScraper

class TruliaHouseListingService():

    def __init__(self, truliaHouseListingDAO: TruliaHouseListingDAO):
        self._truliaHouseListingDAO = truliaHouseListingDAO

    @staticmethod
    def createTruliaHouseListingDataObject(scrapedHomeDict) -> TruliaHouseListing:
        normalizedHomeData = TruliaHouseListingService.normalizehomeDictData(scrapedHomeDict)
        return TruliaHouseListing(**normalizedHomeData)
    
    @staticmethod
    def normalizehomeDictData(homeDictData: dict):
        homeDictDataCopy = copy.deepcopy(homeDictData)
        homeDictDataCopy.pop('url', None)
        homeDictDataCopy['key'] = f'{homeDictDataCopy["address"]}, {homeDictDataCopy["zip"]}'
        if homeDictDataCopy.get('floor_sqft'):
            homeDictDataCopy['floor_sqft'] = int(re.search(r'(\d+)', homeDictDataCopy['floor_sqft']).group(0)) if isinstance(homeDictDataCopy.get('floor_sqft'), str) else homeDictDataCopy['floor_sqft']
        if homeDictDataCopy.get('lot_sqft'):
            homeDictDataCopy['lot_sqft'] = int(re.search(r'(\d+)', homeDictDataCopy['lot_sqft']).group(0)) if isinstance(homeDictDataCopy.get('lot_sqft'), str) else homeDictDataCopy['lot_sqft']
        if homeDictDataCopy.get('date_scraped'):
            homeDictDataCopy['date_scraped'] = datetime.strptime(homeDictDataCopy['date_scraped'], '%Y-%m-%d')
        if homeDictDataCopy.get('date_listed_or_sold'):
            homeDictDataCopy['date_listed_or_sold'] = datetime.strptime(homeDictDataCopy['date_listed_or_sold'], '%Y-%m-%d')
        if homeDictDataCopy.get('year_built'):
            homeDictDataCopy['year_built'] = safeParseInt(homeDictDataCopy['year_built'])
        if homeDictDataCopy.get('year_renovated'):
            homeDictDataCopy['year_renovated'] = safeParseInt(homeDictDataCopy['year_renovated'])
        return homeDictDataCopy
    
    @staticmethod
    def scrapeTruliaData(**kwargs):
        payloadGeneratorHouseScan = PayloadGenerator_HouseScan(**kwargs)
        scraper = TruliaScraper(payloadGeneratorHouseScan)
        scraper.makeRequest()
        dataParserHouseScan = DataParser_HouseScan(scraper.data, scraper.payload)
        scraper.generatePayload(PayloadGenerator_DetailedHouseScraper(dataParserHouseScan.urls))
        scraper.makeRequest()
        dataParserDetailedScrape = DataParser_DetailedScrape(scraper.data, dataParserHouseScan.scrapedHomes)
        return dataParserDetailedScrape
    
    @staticmethod
    def scrapeTruliaRentalData():
        payloadGeneratorHouseScan = PayloadGenerator_HouseScan(searchType='FOR_RENT', limit=100)
        scraper = TruliaScraper(payloadGeneratorHouseScan)
        scraper.makeRequest()
        dataParserHouseScan = DataParser_HouseScan(scraper.data, scraper.payload)
        scraper.generatePayload(PayloadGenerator_DetailedHouseScraper(dataParserHouseScan.urls))
        scraper.makeRequest()
        dataParserDetailedScrape = DataParser_DetailedScrape(scraper.data, dataParserHouseScan.scrapedHomes)
        return dataParserDetailedScrape
    

    def insertNormalizedDataIntoDb(self, truliaNormalizedDataList: list[TruliaHouseListing], searchType: str):
        if searchType.upper() == 'FOR_SALE':
            existingData = self.fetchListingsData()
        elif searchType.upper() == 'FOR_RENT':
            existingData = self.fetchListingsData()
        elif searchType.upper() == 'SOLD':
            existingData = self.fetchSoldData()
        else:
            raise ValueError(f'Invalid search type: {searchType.upper()}')
        dataIndex = {entry['key']: entry for entry in existingData}
        scrapedDataToInsert = []
        scrapedDataToUpdate = []
        for truliaDataObject in truliaNormalizedDataList:
            if dataIndex.get(truliaDataObject.key):
                scrapedDataToUpdate.append(truliaDataObject)
            else:
                scrapedDataToInsert.append(truliaDataObject)
        self._truliaHouseListingDAO.insertMultipleListingsIntoTable(scrapedDataToInsert)
        self._truliaHouseListingDAO.updateMultipleListingsInTable(scrapedDataToUpdate)


    def fetchListingsData(self):
        return self._truliaHouseListingDAO.getAllListings()
    
    def fetchRentalData(self):
        return self._truliaHouseListingDAO.getAllRentals()
    
    def fetchSoldData(self):
        return self._truliaHouseListingDAO.getAllSold()