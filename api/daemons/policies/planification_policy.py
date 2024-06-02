from typing import List
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler


class PlanificationPolicy():
    schedulers: List[Scheduler]
    highest_priority: Scheduler

    def __init__(self, schedulers: List[Scheduler], highest_priority: Scheduler):
        self.schedulers = schedulers
        self.highest_priority = highest_priority

    def apply(self, to_be_queued_jobs: List[Job]):
        ''' Apply the planification policy '''
        raise NotImplementedError
