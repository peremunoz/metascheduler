from typing import List

from api.interfaces.job import Job


class Scheduler:
    '''
    Scheduler interface

    '''

    name: str
    hostname: str
    port: int
    running_jobs: List[Job]

    def __init__(self) -> None:
        self.running_jobs = []

    def update_job_list(self):
        '''
        Update the job list

        '''
        raise NotImplementedError

    def get_job_list(self) -> List[Job]:
        '''
        Check the scheduler queue

        '''
        raise NotImplementedError
