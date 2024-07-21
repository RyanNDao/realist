from backend.scrapers.trulia import constants
import logging
import json
import requests
import copy
from backend.helpers import common_helpers

LOGGER = logging.getLogger(__name__)

queryVariableMapper = {
    'searchType': str,
    'limit': int
}


class PayloadGenerator_HouseScan():
    # pass in key/value pairs with the value being the option

    def __init__(self, **kwargs):
        self.payload = copy.deepcopy(constants.GRAPHQL_HOUSE_SCAN_PAYLOAD_TEMPLATE)
        self.queryVariables = copy.deepcopy(constants.TRULIA_HOUSE_SCAN_DEFAULT_QUERY_VARIABLES)
        self.headers = copy.deepcopy(constants.TRULIA_HEADERS)
        location = self.queryVariables.get('searchDetails', {}).get('location', {})
        if 'zips' in kwargs:
            zipList = kwargs['zips'].split(',')
            for zip in zipList:
                location['zips'].append(zip)
            kwargs.pop('zips')
        else:
            location['cities'].append({
                "city": "Philadelphia",
                "state": "PA"
            })
        for attribute in kwargs:
            if attribute in queryVariableMapper and type(kwargs[attribute]) is not queryVariableMapper[attribute]:
                castType = queryVariableMapper[attribute]
                LOGGER.warning(f'Casting {attribute} from {type(attribute)} to {queryVariableMapper[attribute]}')
                kwargs[attribute] = castType(kwargs[attribute])
            LOGGER.info('Modifying the "{attribute}" attribute to <{newValue}> if the key exists'.format(attribute=attribute, newValue=kwargs[attribute]))
            common_helpers.editQueryVariables(attribute, kwargs[attribute], self.queryVariables)
        self.fillPayloadTemplate()

    def fillPayloadTemplate(self):
        self.payload['query'] = constants.GRAPHQL_HOUSE_SCAN_QUERY
        self.payload['variables'] = self.queryVariables
        self.payload = json.dumps(self.payload)


class PayloadGenerator_DetailedHouseScraper():
    
    def __init__(self, urls: list,  wordsToIncludeInDescription=[], wordsToExcludeInDescription=[]):
        self.payload = copy.deepcopy(constants.GRAPHQL_DETAILED_SCRAPE_PAYLOAD_TEMPLATE)
        self.headers = copy.deepcopy(constants.TRULIA_HEADERS)
        self.requiredWords = wordsToIncludeInDescription
        self.excludedWords = wordsToExcludeInDescription
        self.fillPayloadTemplate(urls)

    def fillPayloadTemplate(self, urls):
        if isinstance(urls, list) and len(urls) > 0 :
            self.payload['variables'] = self.getGraphqlPayloadVariablesString(urls)
            self.payload['query'] = self.getGraphqlPayloadQueryString(urls)
            self.payload = json.dumps(self.payload)
        else:
            LOGGER.error('List of endpoints passed to scraper cannot be blank and must be type array - urls: {urls}'.format(urls=str(urls)))
            raise ValueError('List of endpoints passed to scraper cannot be blank and must be type array.')

    def getGraphqlPayloadVariablesString(self, urls):
        variablesDict = {}
        for idx, url in enumerate(urls):
            variablesDict['url{idx}'.format(idx=idx+1)] = url
        return variablesDict

    def getGraphqlPayloadQueryString(self, urls):
        params = ", ".join([f"$url{i+1}: String!" for i in range(len(urls))])

        queryParts = "\n".join([
        f"""
        homeDetailsByUrl{i+1}: homeDetailsByUrl(url: $url{i+1}) {{
            url
            ...HomeDetailsDescriptionFragment
            ...HomeDetailsListingProviderFragment
            ...HomeDetailsFeaturesFragment
            ...HomeDetailsPriceHistoryFragment
            ...HomeDetailsNeighborhoodOverviewFragment
        }}""" for i in range(len(urls))
        ])
        
        return constants.GRAPHQL_DETAILED_SCRAPE_QUERY_TEMPLATE.format(params=params, queryParts=queryParts).replace('\n', '').replace('\t','    ')

        