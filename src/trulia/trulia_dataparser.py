import json
import logging
from helpers.common_helpers import returnedObjectWithPoppedAttributes
import copy
from collections import OrderedDict
import re
from datetime import datetime
from typing import Callable

LOGGER = logging.getLogger(__name__)

class DataParser():

    def __init__(self, data={}, attributesToPop=[]):
        self.data = data
        self.attributesToPop = attributesToPop

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if isinstance(data, str):
            self._data = json.loads(data)
        elif isinstance(data, dict):
            self._data = data
        elif isinstance(data, type(None)):
            self._data = None
            LOGGER.warning('Data type of TruliaScraper instance has been set to None. Check to see if this is expected')
        else:
            LOGGER.error('Data type of {dataType} is invalid. Convert to dict or string.'.format(dataType=type(data)))
            raise AttributeError('data type is invalid')

    @staticmethod
    def defaultParse(obj: dict, path: list[str], default=None):
        currentLevel = obj
        for key in path:
            if currentLevel:
                currentLevel = currentLevel.get(key, {})
        return currentLevel if currentLevel else default

    @staticmethod
    def getAttribute(obj: dict, path: list[str] | str, default=None, parserFunction: Callable = None, **kwargs):
        parserFunction = parserFunction if parserFunction else DataParser.defaultParse
        try:
            return parserFunction(obj, path, default, **kwargs)
        except Exception as e:
            LOGGER.warning('A(n) {errorType} has occurred while extracting home data: {e} | Path: {path} | Parser Function: {func}'.format(
                errorType = e.__class__.__name__,
                e=e,
                path = path,
                func = parserFunction.__name__
            ))
            return default
        

class HouseScan_DataParser(DataParser):

    def __init__(self, data: dict, payload: dict, attributesToPop=['media', 'displayFlags', 'activeForSaleListing', 'tags', 'isSaveable',
            'preferences', 'providerListingId']):
        super().__init__(data, attributesToPop)
        self.urls = []
        self.searchType = self.getAttribute(payload, ['variables', 'searchDetails', 'searchType'], default='FOR_SALE')
        self.scrapedHomes = self.parseHouseData(copy.deepcopy(self.data))
        
    def __len__(self):
        return len(self.scrapedHomes)

    def parseHouseData(self, houseData):
        scrapedHomes = []
        for home in houseData['data']['searchResultMap']['homes']:
            home = returnedObjectWithPoppedAttributes(home, self.attributesToPop)
            parsedHomeData = self.parseHomeData(home)
            if parsedHomeData:
                scrapedHomes.append(parsedHomeData)
                self.urls.append(parsedHomeData['url'])
        LOGGER.info('Parse finished. There were {numOfScrapedHomes} properties that were successfully parsed.'.format(numOfScrapedHomes=len(scrapedHomes)))
        return scrapedHomes
    
    def extractPrimaryDataFromHome(self, homeData: dict) -> OrderedDict | None: 
        extractedPrimaryData = OrderedDict()
        try:
            extractedPrimaryData['location'] = ' '.join(homeData['location']['fullLocation'].split())
            extractedPrimaryData['address'] = ' '.join(homeData['location']['partialLocation'].split())
            extractedPrimaryData['asking_price'] = int(homeData['price']['formattedPrice'].replace('$', '').replace(',', ''))
            extractedPrimaryData['url'] = homeData['url']
            extractedPrimaryData['trulia_url'] = 'trulia.com' + homeData['url']
            return extractedPrimaryData
        except AttributeError:
            location = homeData.get('location', '')
            if location:
                address = location.get('partialLocation', 'Unknown address')
                LOGGER.warning('{address} could not be added due to missing asking price'.format(address=address))
            else:
                LOGGER.warning('{address} could not be added due to missing address'.format(address=address))
            return None
        except ValueError:
            address = homeData.get('location', {}).get('partialLocation', 'Unknown address')
            LOGGER.warning('{address} was not added due to non-specific asking price'.format(address=address))
            return None

    def extractSupplementaryDataFromHome(self, homeData: dict, parsedHomeData: OrderedDict) -> OrderedDict:
        parsedHomeData['city'] = self.getAttribute(homeData, ['location', 'city'])
        parsedHomeData['state'] = self.getAttribute(homeData, ['location', 'stateCode'])
        parsedHomeData['zip'] = self.getAttribute(homeData, ['location', 'zipCode'])
        parsedHomeData['floor_sqft'] = self.getAttribute(homeData, ['floorSpace', 'formattedDimension'])
        parsedHomeData['lot_size'] = self.getAttribute(homeData, ['lotSize', 'formattedDimension'])
        parsedHomeData['bedrooms'] = self.getAttribute(homeData, ['bedrooms', 'formattedValue'], default=None, parserFunction=self.getBathroomsBedrooms)
        parsedHomeData['bathrooms'] = self.getAttribute(homeData, ['bathrooms', 'formattedValue'], default=None, parserFunction=self.getBathroomsBedrooms)
        parsedHomeData['trulia_listing_id'] = self.getAttribute(homeData, ['metadata', 'legacyIdForSave'])
        parsedHomeData['date_listed_or_sold'] = self.getAttribute(homeData, path=None, default=None, parserFunction=self.getDateListedOrSold, searchType=self.searchType)
        parsedHomeData['listing_status'] = self.getAttribute(homeData, path=None, default='Unknown', parserFunction=self.getListingStatus)
        return parsedHomeData

    def extractTrackingDataFromHome(self, homeData: dict, parsedHomeData: OrderedDict) -> OrderedDict:
        trackingList = homeData['tracking']
        parsedHomeData['neighborhood'] = self.getAttribute(trackingList, 'listingNeighborhood', default=None, parserFunction=self.parseTrackingList)
        parsedHomeData['property_type'] = self.getAttribute(trackingList, 'propertyType', default=None, parserFunction=self.parseTrackingList)
        parsedHomeData['parking'] = self.getAttribute(trackingList, 'Parking', default=None, parserFunction=self.parseMiscItemsInTrackingList)
        parsedHomeData['year_built'] = self.getAttribute(trackingList, 'Year Built', default=None, parserFunction=self.parseMiscItemsInTrackingList)
        return parsedHomeData

    def parseHomeData(self, homeData) -> OrderedDict:
        parsedHomeData = self.extractPrimaryDataFromHome(homeData)
        if parsedHomeData is None:
            return None
        parsedHomeData = self.extractSupplementaryDataFromHome(homeData, parsedHomeData)
        parsedHomeData = self.extractTrackingDataFromHome(homeData, parsedHomeData)
        LOGGER.info('{address} was successfully scraped and parsed!'.format(address=parsedHomeData['address']))
        return parsedHomeData

    @staticmethod
    def getListingStatus(homeData: dict, key=None, default='Unknown') -> str:
        statusMapping = {
            'isRecentlySold': 'Sold',
            'isRecentlyRented': 'Rented',
            'isActiveForRent': 'For Rent',
            'isActiveForSale': 'For Sale',
            'isOffMarket': 'Off Market',
            'isForeclosure': 'Foreclosure'
        }
        currentStatusObject = homeData.get('currentStatus', {})
        for status, outcome in statusMapping.items():
            if currentStatusObject.get(status, False):
                return outcome
        else:
            return default

    @staticmethod
    def parseTrackingList(trackingList: list, key: str, default=None, valueName='value'):
        entryWithKey = list(filter(lambda trackingObject: trackingObject['key'] == key, trackingList))
        if len(entryWithKey) == 1:
            return entryWithKey[0][valueName]
        elif len(entryWithKey) == 0:
            LOGGER.warning('Tracking list did not include key {key}'.format(key=key))
            return default
        else:
            LOGGER.warning('More than one entry with key {key} was found: {entryWithKey}'.format(key=key, entryWithKey=entryWithKey))
            return default
        
    @staticmethod
    def parseMiscItemsInTrackingList(trackingList: list, keyword: str, default: None, miscObjectKey='item', valueName='value'):
        entryWithKey = list(filter(lambda trackingObject: trackingObject['key'] == miscObjectKey, trackingList))
        if len(entryWithKey) == 1:
            match = re.search('(?:^|\W){keyword}:(.*?);'.format(keyword=keyword), entryWithKey[0][valueName])
            return match.group(1) if match else default
        elif len(entryWithKey) == 0:
            LOGGER.warning('Tracking list did not include key {key}'.format(key=miscObjectKey))
            return default
        else:
            LOGGER.warning('More than one entry with key {key} was found: {entryWithKey}'.format(key=miscObjectKey, entryWithKey=entryWithKey))
            return default

    @staticmethod
    def getBathroomsBedrooms(home: dict, path: list[str], default=None) -> str | None:
        currentLevel = home
        for key in path:
            if currentLevel:
                currentLevel = currentLevel.get(key, {})
        if currentLevel and currentLevel.lower() == 'studio':
            return 'studio'
        elif currentLevel:
            return re.sub('[^0-9]', '', currentLevel)
        else:
            return default
        
    @staticmethod
    def getDateListedOrSold(home: dict, path=None, default=None, searchType=''):
        if searchType == 'FOR_SALE':
            return home['activeListing']['dateListed'].split("T")[0]
        elif searchType == 'SOLD':
            return datetime.strptime(home['fullTags'][1]['formattedName'], '%b %d, %Y').strftime('%Y-%m-%d')
        else:
            return default
        
    
class DetailedScrape_DataParser(DataParser):

    def __init__(self, urls: list, attributesToPop=[]):
        super().__init__()
