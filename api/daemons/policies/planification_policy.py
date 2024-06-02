from typing import List
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler


class PlanificationPolicy():
    schedulers: List[Scheduler]

    def __init__(self, schedulers: List[Scheduler]):
        self.schedulers = schedulers

    def apply(self, to_be_queued_jobs: List[Job]):
        ''' Apply the planification policy '''
        raise NotImplementedError
