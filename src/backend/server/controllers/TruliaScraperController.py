from flask import Blueprint, request
from backend.database.services.TruliaHouseListingService import TruliaHouseListingService
from backend.helpers.database_helpers import token_required
from backend.server.utils.ResponseBuilder import ResponseBuilder
from backend.database.services.UserService import UserService
from injector import inject
import logging

LOGGER = logging.getLogger(__name__)
truliaScraperBp = Blueprint('truliaScraperController', import_name=__name__,  url_prefix='/trulia')

class TruliaScraperController():

    @truliaScraperBp.route('/scrape', methods=['GET'])
    @token_required
    @inject
    def scrapeTrulia(trulia_house_listing_service: TruliaHouseListingService):
        truliaData = trulia_house_listing_service.scrapeTruliaData(**dict(request.args.items()))
        for homeData in truliaData.scrapedHomes.values():
            try:
                normalizedHomeData = trulia_house_listing_service.createTruliaHouseListingDataObject(homeData)
                trulia_house_listing_service.insertNormalizedDataIntoDb(normalizedHomeData)
                LOGGER.warning(f'Scraped listing with the key: {normalizedHomeData.key}')
            except Exception as e:
                LOGGER.error(f'The following error occurred in the controller while trying to insert data into DB: {e} for the following data: {normalizedHomeData.dict}')
        return ResponseBuilder.buildSuccessResponse(truliaData.scrapedHomes, 'Scrape successful!')
    
    @truliaScraperBp.route('/get-listings', methods=['GET'])
    @token_required
    @inject
    def getTruliaListings(trulia_house_listing_service: TruliaHouseListingService):
        truliaData = trulia_house_listing_service.fetchListingsData()
        return ResponseBuilder.buildSuccessResponse(truliaData, 'Scrape successful!')
    
    @truliaScraperBp.route('/get-rentals', methods=['GET'])
    @token_required
    @inject
    def getTruliaRentals(trulia_house_listing_service: TruliaHouseListingService):
        truliaData = trulia_house_listing_service.fetchRentalData()
        return ResponseBuilder.buildSuccessResponse(truliaData, 'Scrape successful!')
    