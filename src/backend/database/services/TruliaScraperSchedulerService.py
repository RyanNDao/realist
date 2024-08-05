from datetime import datetime, timedelta, timezone
import os
import random
import logging
import requests

from backend.helpers.database_helpers import generate_token
from backend.server.utils.CommonLogger import CommonLogger
from src.backend.server.utils.celery_tasks import scrapeTruliaBySearchTypeTask, scrapeTruliaByZipcodeTask


class TruliaScraperSchedulerService():

    @staticmethod
    def scheduleTruliaScrapeBySearchType(typesToScrape: list[str]):
        CommonLogger.LOGGER.info('Scraping scheduling of types kicked off!')
        # 1 minute (60,000) - 2 hours (7,200,000)
        TruliaScraperSchedulerService.determineRuntimesToTasks(typesToScrape, scrapeTruliaBySearchTypeTask, 7, 60000, 7200000)


    @staticmethod
    def scheduleTruliaScrapeByZipcodes(zipcodes: list[str]):
        possibleZipCodes = max(len(zipcodes), 5)
        zipcodesToSelect = random.randint(5, possibleZipCodes)
        selectedZipcodes = random.sample(zipcodes, zipcodesToSelect)
        CommonLogger.LOGGER.info(f'Zipcodes being scheduled to be scraped: {selectedZipcodes}')
        # 10 minutes (600,000) - 12 hours (43,200,000)
        TruliaScraperSchedulerService.determineRuntimesToTasks(selectedZipcodes, scrapeTruliaByZipcodeTask, 3, 600000, 43200000)

    @staticmethod
    def determineRuntimesToTasks(listOfArgsToPassToTask: list[object], celeryTaskFunction: callable, maxTimesToRun: int, minDelay: int, maxDelay: int):
        for arg in listOfArgsToPassToTask:
            timesToRunToday = random.randint(1, maxTimesToRun) # random amount of times to run today
            nextRunTime = datetime.now(timezone.utc)
            for _ in range(timesToRunToday):
                ms_delay = random.randint(minDelay, maxDelay) # random delay between 10 minutes to 12 hours
                nextRunTime += timedelta(milliseconds=ms_delay)
                if nextRunTime.day == datetime.now(timezone.utc).day:
                    CommonLogger.LOGGER.warning(f"Scheduling {celeryTaskFunction.__name__} for {arg} at {nextRunTime.strftime('%Y-%m-%d %H:%M:%S')}")
                    celeryTaskFunction.apply_async(args=[arg], eta=nextRunTime)
                else:
                    CommonLogger.LOGGER.warning(f"Stopped scheduling for {arg} as next run time {nextRunTime.strftime('%Y-%m-%d %H:%M:%S')} crosses midnight.")
                    break  # Stop scheduling if the next run time is not today