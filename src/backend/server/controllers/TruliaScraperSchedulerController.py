from flask import Blueprint
from injector import inject
from backend.database.common.constants import PHILADELPHIA_ZIP_CODES
from backend.database.services.TruliaScraperSchedulerService import TruliaScraperSchedulerService
import logging

from backend.helpers.database_helpers import token_required
from backend.server.utils.ResponseBuilder import ResponseBuilder

baseUrl = 'http://localhost:8000'

LOGGER = logging.getLogger(__name__)

truliaScraperSchedulerBp = Blueprint('truliaScraperSchedulerController', import_name=__name__,  url_prefix=None)



class TruliaScraperSchedulerController():
    
    @truliaScraperSchedulerBp.route('/schedule', methods=['GET'])
    @token_required
    @inject
    def schedule_api(trulia_scraper_scheduler_service: TruliaScraperSchedulerService):
        zipcodes_list = PHILADELPHIA_ZIP_CODES
        trulia_scraper_scheduler_service.scheduleScrapesOfZipcodes(zipcodes_list)
        return ResponseBuilder.buildSuccessResponse({}, 'Task scheduling successful!')
        
