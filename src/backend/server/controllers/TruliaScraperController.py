from flask import Blueprint, request
from backend.database.services.TruliaHouseListingService import TruliaHouseListingService
from backend.helpers.database_helpers import token_required
from backend.server.utils.CommonLogger import CommonLogger
from backend.server.utils.ResponseBuilder import ResponseBuilder
from backend.database.services.UserService import UserService
from injector import inject
import logging


truliaScraperBp = Blueprint('truliaScraperController', import_name=__name__,  url_prefix='/trulia')

class TruliaScraperController():

    @truliaScraperBp.route('/scrape', methods=['GET'])
    @token_required
    @inject
    def scrapeTrulia(trulia_house_listing_service: TruliaHouseListingService):
        requestParams = dict(request.args.items())
        truliaData = trulia_house_listing_service.scrapeTruliaData(**requestParams)
        scrapedEntries = []
        for homeData in truliaData.scrapedHomes.values():
            try:
                scrapedEntries.append(trulia_house_listing_service.createTruliaHouseListingDataObject(homeData))
            except Exception as e:
                CommonLogger.LOGGER.error(f'The following error occurred in the controller while trying to insert data into DB: {e} for the following data: {homeData}')
        trulia_house_listing_service.insertNormalizedDataIntoDb(scrapedEntries, requestParams.get('searchType'))
        return ResponseBuilder.buildSuccessResponse(truliaData.scrapedHomes, 'Scrape successful!')

    
    @truliaScraperBp.route('/get-listings', methods=['GET'])
    @token_required
    @inject
    def getTruliaListings(trulia_house_listing_service: TruliaHouseListingService):
        truliaData = trulia_house_listing_service.fetchListingsData()
        return ResponseBuilder.buildSuccessResponse(truliaData, 'Successfully fetched for-sale properties!')
    
    @truliaScraperBp.route('/get-rentals', methods=['GET'])
    @token_required
    @inject
    def getTruliaRentals(trulia_house_listing_service: TruliaHouseListingService):
        truliaData = trulia_house_listing_service.fetchRentalData()
        return ResponseBuilder.buildSuccessResponse(truliaData, 'Successfully fetched rental properties!')
    
    @truliaScraperBp.route('/get-sold', methods=['GET'])
    @token_required
    @inject
    def getTruliaSold(trulia_house_listing_service: TruliaHouseListingService):
        truliaData = trulia_house_listing_service.fetchSoldData()
        return ResponseBuilder.buildSuccessResponse(truliaData, 'Successfully fetched sold properties!')
    