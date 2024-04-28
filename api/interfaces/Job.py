from datetime import datetime

from interfaces.Scheduler import Scheduler


class Job:
    '''
    Job interface

    '''

    def __init__(self, name: str, scheduler: Scheduler):
        self.name = name
        self.scheduler = scheduler
        self.created_at = datetime.now()
