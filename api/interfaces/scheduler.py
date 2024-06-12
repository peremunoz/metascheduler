from typing import List

from api.interfaces.job import Job
from api.interfaces.node import Node


class Scheduler:
    '''
    Scheduler interface

    '''

    name: str
    master_node: Node
    nodes: List[Node]
    running_jobs: List[Job]

    def __init__(self) -> None:
        self.running_jobs = []

    def set_master_node(self, node: Node):
        '''
        Set the master node

        '''
        self.master_node = node

    def set_nodes(self, nodes: List[Node]):
        '''
        Set the nodes

        '''
        self.nodes = nodes

    def update_job_list(self, metascheduler_queue: List[Job] = None):
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

    def adjust_nice_of_all_jobs(self, new_nice: int):
        '''
        Adjust the nice value of all running jobs.

        '''
        raise NotImplementedError
