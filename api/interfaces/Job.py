from datetime import datetime

from interfaces.Scheduler import Scheduler


class Job:
    '''
    Job interface

    '''

    def __init__(self, name: str, scheduler: Scheduler, id: int = None, created_at: datetime = None):
        self.id = id
        self.name = name
        self.scheduler = scheduler
        self.created_at = datetime.now() if created_at is None else created_at
