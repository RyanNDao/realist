import os
import random
from backend.helpers.database_helpers import generate_token
from backend.scrapers.trulia.constants import SEARCH_TYPES
from backend.server.utils.CommonLogger import CommonLogger
from backend.server.utils.ManagedCeleryTask import ManagedTask
from src.backend.server.configurations.celery_conf import celeryApp, inspector
import requests
import logging
import datetime
import redis




baseUrl = 'http://localhost:8000'

def clear_redis():
    # THIS IS ONLY A TEMP FUNCTION SINCE WE DONT USE REDIS FOR ANYTHING EXCEPT SCHEDULING
    # IF REDIS FUNCTIONALITY IS EXTENDED, BE CAREFUL WITH THIS FUNCTION
    r = redis.Redis()
    r.flushdb()  # Clears the entire database

def revokeAllTasks(active=False, scheduled=True, reserved=True, purge=True):
    if purge:
        purgedCount = celeryApp.control.purge()
        CommonLogger.LOGGER.info(f"Purged {purgedCount} tasks from the queue.")
    if active and (active_tasks:=inspector.active()):
        # revoking actives should not be ran inside celeryApp task because it may revoke itself
        for worker, tasks in active_tasks.items():
            CommonLogger.LOGGER.info(f'Found {active_tasks[worker]} number of active tasks to revoke')
            for task in tasks:
                celeryApp.control.revoke(task['id'], terminate=True, signal='SIGUSR1')
    if scheduled and (scheduled_tasks:=inspector.scheduled()):
        for worker, tasks in scheduled_tasks.items():
            CommonLogger.LOGGER.info(f'Found {scheduled_tasks[worker]} number of scheduled tasks to revoke')
            for task in tasks:
                celeryApp.control.revoke(task['request']['id'], terminate=True, signal='SIGUSR1')
    if reserved and (reserved_tasks:= inspector.reserved()):
        for worker, tasks in reserved_tasks.items():
            CommonLogger.LOGGER.info(f'Found {reserved_tasks[worker]} number of reserved tasks to revoke')
            for task in tasks:
                celeryApp.control.revoke(task['id'], terminate=True, signal='SIGUSR1')

@celeryApp.task(bind=True, base=ManagedTask)
def triggerScrapeScheduling(self):
    CommonLogger.LOGGER.info('Kicking off scheduler for scraping...')
    revokeAllTasks()
    backendToken = generate_token('realistBackend', None, os.getenv('JWT_SECRET_KEY'), 60*10)
    headers = {'Authorization': f'Bearer {backendToken}'}
    response = requests.get(f'{baseUrl}/api/schedule', headers=headers)
    CommonLogger.LOGGER.info(response)

@celeryApp.task(bind=True, base=ManagedTask)
def scrapeTruliaByZipcodeTask(self, zipcode: str):
    searchType = random.choice(SEARCH_TYPES)
    CommonLogger.LOGGER.info(f'CRON JOB triggered to scrape {searchType} properties for zipcode: {zipcode}. TIME: {datetime.datetime.now(datetime.timezone.utc)}')
    backendToken = generate_token('realistBackend', None, os.getenv('JWT_SECRET_KEY'), 60*10)
    url = f'{baseUrl}/api/trulia/scrape?zips={zipcode}&limit=100&searchType={searchType}'
    # url = f'{baseUrl}/api/test-error?zipcode={zipcode}'
    headers = {'Authorization': f'Bearer {backendToken}'}
    requests.get(url, headers=headers)
    CommonLogger.LOGGER.debug(f"Successfully scraped listings for zipcode: {zipcode}")

@celeryApp.task(bind=True, base=ManagedTask)
def scrapeTruliaBySearchTypeTask(self, searchType: str):
    CommonLogger.LOGGER.info(f'CRON JOB triggered to scrape {searchType} properties. TIME: {datetime.datetime.now(datetime.timezone.utc)}')
    backendToken = generate_token('realistBackend', None, os.getenv('JWT_SECRET_KEY'), 60*10)
    url = f'{baseUrl}/api/trulia/scrape?limit=100&searchType={searchType}'
    # url = f'{baseUrl}/api/test-error?searchType={searchType}'
    headers = {'Authorization': f'Bearer {backendToken}'}
    requests.get(url, headers=headers)
    CommonLogger.LOGGER.debug(f"Successfully scraped listings for search type: {searchType}")


