from flask import Blueprint
from injector import inject
from backend.database.common.constants import PHILADELPHIA_ZIP_CODES
from backend.database.services.TruliaScraperSchedulerService import TruliaScraperSchedulerService
import logging

from backend.helpers.database_helpers import token_required
from backend.scrapers.trulia.constants import SEARCH_TYPES
from backend.server.utils.ResponseBuilder import ResponseBuilder

baseUrl = 'http://localhost:8000'



truliaScraperSchedulerBp = Blueprint('truliaScraperSchedulerController', import_name=__name__,  url_prefix=None)



class TruliaScraperSchedulerController():
    
    @truliaScraperSchedulerBp.route('/schedule', methods=['GET'])
    @token_required
    @inject
    def schedule_api(trulia_scraper_scheduler_service: TruliaScraperSchedulerService):
        zipcodes_list = PHILADELPHIA_ZIP_CODES
        trulia_scraper_scheduler_service.scheduleTruliaScrapeByZipcodes(zipcodes_list)
        trulia_scraper_scheduler_service.scheduleTruliaScrapeBySearchType(SEARCH_TYPES)
        return ResponseBuilder.buildSuccessResponse({}, 'Task scheduling successful!')
        
