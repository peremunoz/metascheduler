from typing import List
from api.constants.job_status import JobStatus
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler


class SGE(Scheduler):
    '''
    SGE Scheduler

    '''

    def __init__(self) -> None:
        super().__init__()
        self.name = 'SGE'

    def __str__(self) -> str:
        return f'SGE Scheduler: {self.hostname}:{self.port}'

    def update_job_list(self):
        '''
        Update the job list

        '''
        self.running_jobs = [
            Job(id_='1', name='job1', owner='root', status=JobStatus.RUNNING),
            Job(id_='2', name='job2', owner='root', status=JobStatus.QUEUED),
            Job(id_='3', name='job3', owner='root', status=JobStatus.QUEUED),
        ]
        return

        qstat = self._call_qstat()
        jobs = self._parse_qstat(qstat)
        self.running_jobs = jobs

    def get_job_list(self) -> List[Job]:
        '''
        Get the list of jobs from the SGE scheduler

        '''
        return self.running_jobs

    def _call_qstat(self) -> str:
        '''
        TODO:
        Call the qstat command to get the list of jobs

        '''
        raise NotImplementedError

    def _parse_qstat(self, qstat_output) -> List[Job]:
        '''
        TODO:
        Parse the output of the qstat command

        '''
        raise NotImplementedError
