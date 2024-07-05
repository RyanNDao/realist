import json
import logging
from backend.helpers.common_helpers import returnedObjectWithPoppedAttributes
import copy
from collections import OrderedDict
import re
from datetime import datetime
from typing import Callable
from backend.exceptions import DataParsingError

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
            LOGGER.warning('Data type of DataParser instance has been set to None. Check to see if this is expected')
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
    def getAttribute(obj: dict, path: list[str] | str, default=None, parserFunction: Callable = None, mustReturnSomething: bool = False, **kwargs):
        parserFunction = parserFunction if parserFunction else DataParser.defaultParse
        try:
            returnedAttribute = parserFunction(obj, path, default, **kwargs)
            if (returnedAttribute == None) and mustReturnSomething:
                raise Exception('Nothing was returned while parsing even though something was expected!')
            return returnedAttribute
        except Exception as e:
            LOGGER.warning('A(n) {errorType} has occurred while extracting home data: {e} | Path: {path} | Parser Function: {func}'.format(
                errorType = e.__class__.__name__,
                e=e,
                path = path,
                func = parserFunction.__name__
            ))
            if mustReturnSomething:
                raise Exception(e)
            return default
        

class DataParser_HouseScan(DataParser):

    def __init__(self, data: dict, payload: dict | str, attributesToPop=['media', 'displayFlags', 'activeForSaleListing', 'tags', 'isSaveable',
            'preferences', 'providerListingId']):
        super().__init__(data, attributesToPop)
        self.urls = []
        self.searchType = self.getAttribute(payload if type(payload) == dict else json.loads(payload) , ['variables', 'searchDetails', 'searchType'], default='FOR_SALE')
        self.scrapedHomes = self.parseHouseData(copy.deepcopy(self.data))
        
    def __len__(self):
        return len(self.scrapedHomes)

    def parseHouseData(self, listingsData):
        scrapedHomes = {}
        for home in listingsData['data']['searchResultMap']['homes']:
            home = returnedObjectWithPoppedAttributes(home, self.attributesToPop) #less objects to look at while debugging
            parsedHomeData = self.parseHomeData(home)
            if parsedHomeData:
                scrapedHomes[parsedHomeData['url']] = parsedHomeData
                self.urls.append(parsedHomeData['url'])
        LOGGER.info('Parse finished. There were {numOfScrapedHomes} properties that were successfully parsed.'.format(numOfScrapedHomes=len(scrapedHomes)))
        return scrapedHomes
    
    def parseHomeData(self, homeData) -> OrderedDict:
        if (parsedHomeData:= self.extractPrimaryDataFromHome(homeData)) is None:
            return None
        parsedHomeData = self.extractSupplementaryDataFromHome(homeData, copy.deepcopy(parsedHomeData))
        parsedHomeData = self.extractTrackingDataFromHome(homeData, copy.deepcopy(parsedHomeData))
        LOGGER.info('{address} was successfully scraped and parsed!'.format(address=parsedHomeData['address']))
        return parsedHomeData
    
    def extractPrimaryDataFromHome(self, homeData: dict) -> OrderedDict | None: 
        extractedPrimaryData = OrderedDict()
        try:
            extractedPrimaryData['location'] = ' '.join(homeData['location']['fullLocation'].split())
            extractedPrimaryData['address'] = ' '.join(homeData['location']['partialLocation'].split())
            extractedPrimaryData['asking_price'] = int(homeData['price']['formattedPrice'].replace('$', '').replace(',', '').replace('/mo',''))
            extractedPrimaryData['url'] = homeData['url']
            extractedPrimaryData['trulia_url'] = 'trulia.com' + homeData['url']
            extractedPrimaryData['zip'] = self.getAttribute(homeData, ['location', 'zipCode'], mustReturnSomething=True)
            return extractedPrimaryData
        except AttributeError:
            if location:= homeData.get('location', ''):
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
        parsedHomeData['floor_sqft'] = self.getAttribute(homeData, ['floorSpace', 'formattedDimension'])
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
            LOGGER.warning(f'Tracking list did not include key {key}')
            return default
        else:
            LOGGER.warning(f'More than one entry with key {key} was found: {entryWithKey}')
            return default
        
    @staticmethod
    def parseMiscItemsInTrackingList(trackingList: list, keyword: str, default: None, miscObjectKey='item', valueName='value'):
        entryWithKey = list(filter(lambda trackingObject: trackingObject['key'] == miscObjectKey, trackingList))
        if len(entryWithKey) == 1:
            match = re.search(rf'(?:^|\W){keyword}:(.*?);', entryWithKey[0][valueName])
            return match.group(1) if match else default
        elif len(entryWithKey) == 0:
            LOGGER.warning(f'Tracking list did not include key {miscObjectKey}')
            return default
        else:
            LOGGER.warning(f'More than one entry with key {miscObjectKey} was found: {entryWithKey}')
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
            return re.sub('[^0-9.]', '', currentLevel)
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
    
class DataParser_DetailedScrape(DataParser):

    def __init__(self, dataToParse: dict, scrapedHomes: dict[OrderedDict], attributesToPop=[]):
        super().__init__(dataToParse, attributesToPop)
        self.scrapedHomes = self.parseHouseData(copy.deepcopy(self.data), copy.deepcopy(scrapedHomes))

    def __len__(self):
        return len(self.scrapedHomes)

    @property
    def scrapedHomes(self):
        return self._scrapedHomes
    
    @scrapedHomes.setter
    def scrapedHomes(self, scrapedHomes: dict[OrderedDict]):
        if isinstance(scrapedHomes, dict) and all(isinstance(home, OrderedDict) for home in scrapedHomes.values()):
            self._scrapedHomes = scrapedHomes
        elif isinstance(scrapedHomes, dict):
            LOGGER.warning('Could not assign scraped homes to DataParser_DetailedScrape, object needs to be a dict of OrderedDict.')
            LOGGER.warning('Element types of object indices: {scrapedHomesTypes}'.format(scrapedHomesTypes=[type(home) for home in scrapedHomes.values()]))
        else:
            LOGGER.warning('Could not assign scraped homes to DataParser_DetailedScrape, object needs to be a dict of OrderedDict.')

    def parseHouseData(self, listingsData: dict, scrapedHomes: dict[OrderedDict]):
        for homeData in listingsData['data'].values():
            try:
                associatedHome, url = self.returnAssociatedScrapedHome(homeData, scrapedHomes)
            except DataParsingError as e:
                LOGGER.warning(str(e))
                continue
            associatedHome = self.extractFeaturesData(homeData, copy.deepcopy(associatedHome))
            associatedHome = self.extractAdditionalDetailedData(homeData, copy.deepcopy(associatedHome))
            scrapedHomes.update({url: associatedHome})
            LOGGER.info('Scrape successful for listing with the following url: {url}'.format(url=url))
        return scrapedHomes

    def extractAdditionalDetailedData(self, homeData: dict, associatedHome: OrderedDict):
        associatedHome['description'] = self.getAttribute(homeData, ['description', 'value'], default='No description found')
        if priceHistory := self.getAttribute(homeData, ['priceHistory']):
            associatedHome['price_history'] = [returnedObjectWithPoppedAttributes(event,['__typename', 'source', 'mlsLogo', 'attributionSource', 'attributes']) for event in priceHistory]
        if not associatedHome['neighborhood']:
            associatedHome['neighborhood'] = self.getAttribute(homeData, ['surroundings','name'])
        return associatedHome
    
    def extractFeaturesData(self, homeData: dict, associatedHome: OrderedDict):
        featuresData = homeData.get('features', {})
        if featuresData:
            associatedHome['basement'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Interior Features', 'categories'),
                ('formattedName', 'Interior Details', 'attributes'),
                ('formattedName', 'Basement', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['floor_sqft'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Interior Features', 'categories'),
                ('formattedName', 'Dimensions and Layout', 'attributes'),
                ('formattedName', 'Living Area', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['foundation'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Exterior Features', 'categories'),
                ('formattedName', 'Exterior Home Features', 'attributes'),
                ('formattedName', 'Foundation', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['parking'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Exterior Features', 'categories'),
                ('formattedName', 'Parking & Garage', 'attributes'),
                ('formattedName', 'Parking', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['days_on_market'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Days on Market', 'attributes'),
                ('formattedName', 'Days on Market', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['year_built'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Property Information', 'categories'),
                ('formattedName', 'Year Built', 'attributes'),
                ('formattedName', 'Year Built', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['year_renovated'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Property Information', 'categories'),
                ('formattedName', 'Year Built', 'attributes'),
                ('formattedName', 'Year Renovated', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['property_subtype'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Property Information', 'categories'),
                ('formattedName', 'Property Type / Style', 'attributes'),
                ('formattedName', 'Property Subtype', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['structure_type'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Property Information', 'categories'),
                ('formattedName', 'Property Type / Style', 'attributes'),
                ('formattedName', 'Structure Type', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['architecture'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Property Information', 'categories'),
                ('formattedName', 'Property Type / Style', 'attributes'),
                ('formattedName', 'Architecture', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['house_material'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Property Information', 'categories'),
                ('formattedName', 'Building', 'attributes'),
                ('formattedName', 'Construction Materials', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['parcel_number'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Property Information', 'categories'),
                ('formattedName', 'Property Information', 'attributes'),
                ('formattedName', 'Parcel Number', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['condition'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Property Information', 'categories'),
                ('formattedName', 'Property Information', 'attributes'),
                ('formattedName', 'Condition', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['lot_sqft'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Lot Information', 'attributes'),
                ('formattedName', 'Lot Area', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            associatedHome['mls_listing_id'] = self.getAttribute(featuresData, [
                'categories', 
                ('formattedName', 'Agent Information', 'categories'),
                ('formattedName', 'Listing Agent', 'attributes'),
                ('formattedName', 'Listing ID', 'formattedValue')
            ], None, parserFunction=self.getFeature)
            if associatedHome['floor_sqft']:
                associatedHome['floor_sqft'] = associatedHome['floor_sqft'].lower().replace('square feet', 'sqft')
            if associatedHome['lot_sqft']:
                associatedHome['lot_sqft'] = associatedHome['lot_sqft'].lower().replace('square feet', 'sqft')
        return associatedHome

    @staticmethod
    def returnAssociatedScrapedHome(homeData: dict, scrapedHomes: dict[OrderedDict]) -> OrderedDict:
        if not (url:= homeData.get('url', None)):
            raise DataParsingError('Home data does not have url attribute: {data}'.format(data=homeData))
        associatedScrapedHome = scrapedHomes.get(url, None)
        if associatedScrapedHome == None:
            raise DataParsingError('List of scraped house_scan data does not have the url: {url}'.format(url=url))
        return associatedScrapedHome, url

    @staticmethod
    def getFeature(home: dict, path=list[str|tuple], default=None):
        currentLevel = home
        for level in path:
            if isinstance(level, str):
                currentLevel = currentLevel.get(level, {})
            elif isinstance(level, tuple) and len(level) == 3:
                # index 0 = search all elements for this key
                # index 1 = the value that the key should match
                # index 2 = if object is found, set currentLevel to the value of the given key
                foundObject = next((element for element in currentLevel if element.get(level[0], None) == level[1]), {})
                currentLevel = foundObject.get(level[2], {})
            else:
                LOGGER.warning('The element, {invalidLevel}, in path is invalid. Returning default.'.format(invalidLevel=level))
                return default
        return currentLevel if currentLevel and path else default
    

    
