from datetime import datetime, timedelta, timezone
import os
import random
import logging
import requests

from backend.helpers.database_helpers import generate_token
from src.backend.server.utils.celery_tasks import scrapeZipcodeTask
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class TruliaScraperSchedulerService():

    @staticmethod
    def scheduleScrapesOfZipcodes(zipcodes):
        LOGGER.info('Scraping scheduling kicked off!!')
        possibleZipCodes = max(len(zipcodes) - 15, 5)
        zipcodesToSelect = random.randint(3, possibleZipCodes)
        selectedZipcodes = random.sample(zipcodes, zipcodesToSelect)
        LOGGER.info(f'Chosen zipcodes: {selectedZipcodes}')

        for zipcode in selectedZipcodes:
            timesToRunToday = random.randint(1, 3) # random amount of times to run today
            nextRunTime = datetime.now(timezone.utc)
            for _ in range(timesToRunToday):
                ms_delay = random.randint(60000, 100000) # random delay between 10 minutes to 12 hours
                nextRunTime += timedelta(milliseconds=ms_delay)
                if nextRunTime.day == datetime.now(timezone.utc).day:
                    LOGGER.info(f"Scheduling 'scrape_function' for zipcode {zipcode} at {nextRunTime.strftime('%Y-%m-%d %H:%M:%S')}")
                    scrapeZipcodeTask.apply_async(args=[zipcode], eta=nextRunTime)
                else:
                    LOGGER.info(f"Stopped scheduling for zipcode {zipcode} as next run time {nextRunTime.strftime('%Y-%m-%d %H:%M:%S')} crosses midnight.")
                    break  # Stop scheduling if the next run time is not today