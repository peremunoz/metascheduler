from datetime import datetime

from api.constants.job_status import JobStatus


class Job:
    '''
    Job interface

    '''

    def __init__(self, id: int = None, queue: int = -1, name: str = None,
                 created_at: datetime = None, owner: str = None,
                 status: JobStatus = JobStatus.QUEUED):
        self.id = id
        self.queue = queue
        self.name = name
        self.created_at = datetime.now() if created_at is None else created_at
        self.owner = owner
        self.status = status
