import os
from celery import Celery
from celery.schedules import crontab
import logging
from dotenv import load_dotenv
load_dotenv()

LOGGER = logging.getLogger(__name__)

def initCelery(app=None) -> Celery:
    celery = Celery(__name__, 
        broker=os.getenv('CELERY_BROKER_URL'), 
        backend=os.getenv('CELERY_BACKEND_URL'),
        include=['src.backend.server.utils.celery_tasks']
    )
    if app is not None:
        celery.conf.update(app.config)
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        celery.Task = ContextTask
        celery.control.purge()

    celery.conf.timezone = 'America/New_York' 
    celery.conf.beat_schedule = {
        'trigger_schedule_every_midnight': {
            'task': 'src.backend.server.utils.celery_tasks.triggerScrapeScheduling',
            'schedule': crontab(hour=0, minute=0)  # Executes at midnight New York time
    }
}
    return celery

celeryApp = initCelery()
inspector = celeryApp.control.inspect()