from typing import List
from api.interfaces.scheduler import Scheduler


class PlanificationPolicy():
    schedulers: List[Scheduler]

    def __init__(self, schedulers: List[Scheduler]):
        self.schedulers = schedulers

    def apply(self, metascheduler_queue: List[Scheduler]):
        ''' Apply the planification policy '''
        raise NotImplementedError
