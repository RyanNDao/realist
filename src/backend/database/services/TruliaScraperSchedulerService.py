import datetime
import os
import random
import logging
import requests

from backend.helpers.database_helpers import generate_token
from backend.server.utils.Scheduler import scheduler

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

baseUrl = 'http://localhost:8000'


def scrape_function(zipcode):
    searchType = random.choice(['FOR_SALE', 'FOR_RENT'])
    LOGGER.info(f'CRON JOB triggered to scrape {searchType} properties for zipcode: {zipcode} ')
    backendToken = generate_token('realistBackend', None, os.getenv('JWT_SECRET_KEY'), 60*10)
    url = f'{baseUrl}/api/trulia/scrape?zips={zipcode}&limit=100&searchType={searchType}'
    headers = {'Authorization': f'Bearer {backendToken}'}
    # requests.get(url, headers=headers)
    LOGGER.info(f"Successfully scraped listings for zipcode: {zipcode}")

class TruliaScraperSchedulerService():

    def scheduleTasks(self, zipcodes):
        possibleZipCodes = len(zipcodes) - 2000
        zipcodesToSelect = random.randint(3, possibleZipCodes) if possibleZipCodes > 3 else 3
        selectedZipcodes = random.sample(zipcodes, zipcodesToSelect)
        LOGGER.info(f'Chosen zipcodes: {selectedZipcodes}')
        for zipcode in selectedZipcodes:
            self.scheduleTaskForZipcode(zipcode)

    def scheduleTaskForZipcode(self, zipcode):
        timesToRunToday = random.randint(0, 1)
        LOGGER.info(f"Zipcode {zipcode} will run a maximum of {timesToRunToday} times today.")
        nextRunTime = datetime.datetime.now()

        for _ in range(timesToRunToday):
            ms_delay = random.randint(0, 21600)  # Random delay in milliseconds, 15 minutes - 6 hours
            nextRunTime += datetime.timedelta(milliseconds=ms_delay)

            if nextRunTime.date() > datetime.datetime.now().date():
                break

            LOGGER.info(f"Task for zipcode {zipcode} scheduled at {nextRunTime.strftime('%Y-%m-%d %H:%M:%S')}.")
            scheduler.add_job(scrape_function, 'date', run_date=nextRunTime, args=[zipcode], replace_existing=True, id=f'scrape_{zipcode}_{nextRunTime}')
