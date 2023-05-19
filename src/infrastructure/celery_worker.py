from celery import Celery

from core.settings import settings
from models.task import JobType
from use_cases.abstract_worker import AbstractWorker

app = Celery('profile-worker')

app.conf.broker_url = settings.storage_url

app.conf.task_default_queue = 'profiles'

app.conf.timezone = 'UTC'


class CeleryWorker(AbstractWorker):
    def start_job(self, *, job_type: JobType, **kwargs):
        app.signature(f'tasks.{job_type.value}', kwargs=kwargs).apply_async()
