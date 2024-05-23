from typing import List
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler


class ApacheHadoop(Scheduler):
    '''
    Apache Hadoop Scheduler

    '''

    running_job: Job

    def __init__(self) -> None:
        super().__init__()
        self.name = 'Apache Hadoop'
        self.running_job = None

    def __str__(self) -> str:
        return f'Apache Hadoop Scheduler: {self.hostname}:{self.port}'

    def get_job_list(self) -> List[Job]:
        '''
        Get the list of jobs from the Apache Hadoop scheduler

        As Apache Hadoop does not have a scheduler, this method will return the actual running job, if any.

        '''
        return [self.running_job]
