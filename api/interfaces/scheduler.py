from typing import List

from api.interfaces.job import Job


class Scheduler:
    '''
    Scheduler interface

    '''

    name: str
    hostname: str
    port: int

    def get_job_list(self) -> List[Job]:
        '''
        Check the scheduler queue

        '''
        raise NotImplementedError
