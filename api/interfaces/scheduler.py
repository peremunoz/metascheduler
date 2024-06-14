from typing import List, Tuple

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
    weight: int

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

    def set_weight(self, weight: int):
        '''
        Set the weight of the scheduler

        '''
        self.weight = weight

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

    def adjust_nice_of_job(self, job_pid: int, new_nice: int):
        '''
        Adjust the nice value of a running job.

        '''
        raise NotImplementedError

    def get_all_jobs_info(self) -> List[Tuple[int, int, float, float]]:
        '''
        Get the information of all running jobs.
        Being: job_pid, job_nice, job_cpu_usage, job_memory_usage

        '''
        raise NotImplementedError
