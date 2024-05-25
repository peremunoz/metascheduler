from typing import List
from api.constants.job_status import JobStatus
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler
from api.routers.jobs import PutJobModel

JOB_RUNNING = PutJobModel(status=JobStatus.RUNNING)
JOB_COMPLETED = PutJobModel(status=JobStatus.COMPLETED)


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
        Update the job list.
        Also update the job status in the database.

        '''
        self.running_jobs = [
            Job(id_='1', name='job1', owner='root', status=JobStatus.RUNNING),
            Job(id_='2', name='job2', owner='root', status=JobStatus.QUEUED),
            Job(id_='3', name='job3', owner='root', status=JobStatus.QUEUED),
        ]
        return

        qstat = self._call_qstat()
        jobs = self._parse_qstat(qstat)
        for job in jobs:
            if job.status == JobStatus.QUEUED:
                continue
            job_update_status = JOB_RUNNING if job.status == JobStatus.RUNNING else JOB_COMPLETED
            update_job(job.id_, job.owner, job_update_status)
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

    def queue_job(self, job: Job):
        '''
        Queue a job

        '''
        self._call_qsub(job)
        self.running_jobs.append(job)

    def _call_qsub(self, job: Job):
        '''
        TODO:
        Call the qsub command to queue the job

        '''
        return
        raise NotImplementedError
