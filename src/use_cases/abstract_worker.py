from abc import ABC, abstractmethod

from models.task import JobType


class AbstractWorker(ABC):
    @abstractmethod
    def start_job(self, *, job_type: JobType, **kwargs):
        pass
