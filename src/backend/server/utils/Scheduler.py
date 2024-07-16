import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


scheduler = BackgroundScheduler(jobstores={
    'default': SQLAlchemyJobStore(url=os.getenv('SQLALCHEMY_CONNECTION_STRING_TEMPLATE').format('users'))
})