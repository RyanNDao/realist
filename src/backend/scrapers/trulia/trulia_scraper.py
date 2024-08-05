from backend.scrapers.trulia import constants
import copy
from backend.helpers import common_helpers
from backend.scrapers.trulia.trulia_payloadgenerator import PayloadGenerator_HouseScan, PayloadGenerator_DetailedHouseScraper
import logging
import requests
import os
import json

from backend.server.utils.CommonLogger import CommonLogger



class TruliaScraper():

    def __init__(self, payloadGenerator: PayloadGenerator_HouseScan | PayloadGenerator_DetailedHouseScraper, scrapeUrl=''):
        self.headers = copy.deepcopy(constants.TRULIA_HEADERS)
        self.url = scrapeUrl if scrapeUrl else os.getenv('TRULIA_ENDPOINT_URL', '')
        self.payloadGenerator = payloadGenerator
        self.generatePayload(self.payloadGenerator)
        CommonLogger.LOGGER.debug('Trulia scraper object initialized with payload type {scraperType}, url loaded is: {url}'.format(scraperType=payloadGenerator.__class__.__name__,url=self.url))
        self._data = None

    def makeRequest(self) -> None:
        response = self.returnResponse()
        if response.status_code == 200:
            self.data = response.text
        else:
            self.data = None
            CommonLogger.LOGGER.warning('Code [{statusCode}]: {text}'.format(statusCode=response.status_code, text=response.text))

    def returnResponse(self):
        return requests.request(
            "POST", 
            url=self.url, 
            headers=self.headers, 
            data=self.payload, 
            verify=False
        )

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
            CommonLogger.LOGGER.warning('Data type of TruliaScraper instance has been set to None. Check to see if this is expected')
        else:
            CommonLogger.LOGGER.error('Data type of {dataType} is invalid. Convert to dict or string.'.format(dataType=type(data)))
            raise AttributeError('data type is invalid')

    @property
    def payloadGenerator(self):
        return self._payloadGenerator

    @payloadGenerator.setter
    def payloadGenerator(self, payloadGenerator: PayloadGenerator_HouseScan | PayloadGenerator_DetailedHouseScraper):
        if (isinstance(payloadGenerator, (PayloadGenerator_HouseScan, PayloadGenerator_DetailedHouseScraper))):
            self._payloadGenerator = payloadGenerator
        else:
            CommonLogger.LOGGER.error('Payload generator type of {dataType} is invalid. It should be an instance of a PayloadGenerator class'.format(dataType=type(payloadGenerator)))
            raise AttributeError('payloadGenerator type is invalid')
    
    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, payload):
        self._payload = payload

    def generatePayload(self, payloadGenerator: PayloadGenerator_HouseScan | PayloadGenerator_DetailedHouseScraper):
        if isinstance(payloadGenerator, (PayloadGenerator_HouseScan, PayloadGenerator_DetailedHouseScraper)):
            self.payload = payloadGenerator.payload
        else:
            CommonLogger.LOGGER.error('Argument passed is not of type PayloadGenerator, instead it is {dataType}. Could not extract payload.'.format(dataType=type(payloadGenerator)))

    
    


        
        
        
        
        

    


