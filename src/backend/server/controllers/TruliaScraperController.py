from flask import Blueprint, request
from backend.database.services.TruliaHouseListingService import TruliaHouseListingService
from backend.server.utils.ResponseBuilder import ResponseBuilder
from backend.database.services.UserService import UserService
from injector import inject
import logging

LOGGER = logging.getLogger(__name__)
truliaScraperBp = Blueprint('truliaScraperController', import_name=__name__,  url_prefix='/trulia')

class TruliaScraperController():

    @truliaScraperBp.route('/scrape/for_sale', methods=['GET'])
    @inject
    def scrapeTrulia(trulia_house_listing_service: TruliaHouseListingService):
        truliaData = trulia_house_listing_service.scrapeTruliaData()
        for homeData in truliaData.scrapedHomes.values():
            try:
                normalizedHomeData = trulia_house_listing_service.createTruliaHouseListingDataObject(homeData)
                trulia_house_listing_service.insertNormalizedDataIntoDb(normalizedHomeData)
                LOGGER.info(f'Scraped listing with the key: {normalizedHomeData.key}')
            except Exception as e:
                LOGGER.error(f'The following error occurred in the controller while trying to insert data into DB: {e} for the following data: {normalizedHomeData.dict}')
        return ResponseBuilder.buildSuccessResponse(truliaData.scrapedHomes, 'Scrape successful!')
    

    @truliaScraperBp.route('/scrape/for_rent', methods=['GET'])
    @inject
    def scrapeTruliaRentals(trulia_house_listing_service: TruliaHouseListingService):
        truliaData = trulia_house_listing_service.scrapeTruliaRentalData()
        for homeData in truliaData.scrapedHomes.values():
            LOGGER.warning(homeData)
            try:
                normalizedHomeData = trulia_house_listing_service.createTruliaHouseListingDataObject(homeData)
                trulia_house_listing_service.insertNormalizedDataIntoDb(normalizedHomeData)
                LOGGER.info(f'Scraped listing with the key: {normalizedHomeData.key}')
            except Exception as e:
                LOGGER.error(f'The following error occurred in the controller while trying to insert data into DB: {e} for the following data: {normalizedHomeData.dict}')
        return ResponseBuilder.buildSuccessResponse(truliaData.scrapedHomes, 'Scrape successful!')
