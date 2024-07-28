from celery import Task
from celery.exceptions import SoftTimeLimitExceeded
import logging
LOGGER = logging.getLogger(__name__)

class ManagedTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        if isinstance(exc, SoftTimeLimitExceeded):
            LOGGER.error(f'Task {task_id} was terminated')
        else:
            LOGGER.error(f'Task {task_id} failed: {exc} | {einfo}')

    def on_success(self, retval, task_id, args, kwargs):
        LOGGER.info(f'Task {task_id} completed successfully!!')

    def on_revoked(self):
        LOGGER.info('Task was revoked before starting. Cleanup could be done here.')

    def __call__(self, *args, **kwargs):
        try:
            return super().__call__(*args, **kwargs)
        except SoftTimeLimitExceeded:
            self.on_failure(SoftTimeLimitExceeded("Task was terminated via revoke. Task timed out, which is expected"), self.request.id, args, kwargs, None)