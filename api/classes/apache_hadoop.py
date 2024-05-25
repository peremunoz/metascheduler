from typing import List
from api.constants.job_status import JobStatus
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler
from api.routers.jobs import update_job_status


class ApacheHadoop(Scheduler):
    '''
    Apache Hadoop Scheduler

    '''

    def __init__(self) -> None:
        super().__init__()
        self.name = 'Apache Hadoop'

    def __str__(self) -> str:
        return f'Apache Hadoop Scheduler: {self.hostname}:{self.port}'

    def update_job_list(self):
        '''
        Update the job list.
        Also update the job status in the database.

        As Apache Hadoop does not have a scheduler, this method is not implemented.

        '''
        pass

    def get_job_list(self) -> List[Job]:
        '''
        Get the list of jobs from the Apache Hadoop scheduler.

        As Apache Hadoop does not have a scheduler, this method will return the actual running job, if any.

        '''
        return self.running_jobs

    def queue_job(self, job: Job):
        '''
        Queue a job.

        As Apache Hadoop does not have a scheduler, this method will run the job immediately.

        '''
        self._call_yarn_jar(job)
        if len(self.running_jobs) == 0:
            self.running_jobs.append(job)
        else:
            ended_job = self.running_jobs[0]
            update_job_status(ended_job.id_, ended_job.owner,
                              JobStatus.COMPLETED)
            self.running_jobs[0] = job

        update_job_status(job.id_, job.owner, JobStatus.RUNNING)

    def _call_yarn_jar(self, job: Job):
        '''
        TODO:
        Call the yarn jar command to run the job.

        '''
        return
        raise NotImplementedError
