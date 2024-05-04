from datetime import datetime
from pathlib import Path

from api.constants.job_status import JobStatus


class Job:
    '''
    Job interface

    '''

    def __init__(self, id_: int = None, queue: int = -1, name: str = None,
                 created_at: datetime = None, owner: str = None,
                 status: JobStatus = JobStatus.QUEUED, path: Path = None,
                 options: str = ''):
        self.id_ = id_
        self.queue = queue
        self.name = name
        self.created_at = datetime.now() if created_at is None else created_at
        self.owner = owner
        self.status = status
        self.path = path
        self.options = options
