from typing import List

from api.interfaces.job import Job
from api.interfaces.node import Node


class Scheduler:
    '''
    Scheduler interface

    '''

    name: str
    master_node: Node
    running_jobs: List[Job]

    def __init__(self) -> None:
        self.running_jobs = []

    def set_master_node(self, node: Node):
        '''
        Set the master node

        '''
        self.master_node = node

    def update_job_list(self):
        '''
        Update the job list
        Also update the job status in the database

        '''
        raise NotImplementedError

    def get_job_list(self) -> List[Job]:
        '''
        Check the scheduler queue

        '''
        raise NotImplementedError

    def queue_job(self, job: Job):
        '''
        Queue a job

        '''
        raise NotImplementedError
