from flask import Blueprint
from injector import inject
import requests
import os
from backend.database.common.constants import PHILADELPHIA_ZIP_CODES
from backend.database.services.TruliaScraperSchedulerService import TruliaScraperSchedulerService
from backend.helpers.database_helpers import generate_token
import datetime
import random
import logging
from sqlalchemy import create_engine

from backend.server.utils.ResponseBuilder import ResponseBuilder

baseUrl = 'http://localhost:8000'

LOGGER = logging.getLogger(__name__)

truliaScraperSchedulerBp = Blueprint('truliaScraperSchedulerController', import_name=__name__,  url_prefix=None)



class TruliaScraperSchedulerController():
    
    @truliaScraperSchedulerBp.route('/schedule', methods=['GET'])
    @inject
    def schedule_api(trulia_scraper_scheduler_service: TruliaScraperSchedulerService):
        zipcodes_list = PHILADELPHIA_ZIP_CODES
        trulia_scraper_scheduler_service.scheduleTasks(zipcodes_list)
        return ResponseBuilder.buildSuccessResponse({}, 'Task scheduling successful!')
        
