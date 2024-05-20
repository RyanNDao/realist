from backend.database.models.TruliaHouseListing import TruliaHouseListing
from backend.database.dao.TruliaHouseListingDAO import TruliaHouseListingDAO
import copy
import re
from datetime import datetime, date

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
        if homeDictDataCopy.get('date_listed_or_sold'):
            homeDictDataCopy['date_listed_or_sold'] = datetime.strptime(homeDictDataCopy['date_listed_or_sold'], '%Y-%m-%d')
        if homeDictDataCopy.get('year_built'):
            homeDictDataCopy['year_built'] = int(homeDictDataCopy['year_built'])
        if homeDictDataCopy.get('year_renovated'):
            homeDictDataCopy['year_renovated'] = int(homeDictDataCopy['year_renovated'])
        return homeDictDataCopy