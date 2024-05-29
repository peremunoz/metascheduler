from enum import Enum


class JobStatus(Enum):
    TO_BE_QUEUED = 'TO_BE_QUEUED'
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    ERROR = 'ERROR'
