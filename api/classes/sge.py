from typing import List
from api.constants.job_status import JobStatus
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler
from api.routers.jobs import set_job_scheduler_job_id, update_job_status
import xml.etree.ElementTree as ET

SGE_ROOT = '/opt/sge/'
QSTAT = SGE_ROOT + 'bin/lx-amd64/qstat'
QSUB = SGE_ROOT + 'bin/lx-amd64/qsub'


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

        # qstat = self._call_qstat()
        # jobs = self._parse_qstat(qstat)
        jobs = [
            Job(id_=1, queue=1, name='claudia',
                owner='peremunoz', status=JobStatus.RUNNING),
        ]
        for job in jobs:
            if job.status == JobStatus.QUEUED:
                continue
            update_job_status(job.id_, job.owner, job.status)
            set_job_scheduler_job_id(job.id_, job.owner, 14)
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
        qstat_xml = self.master_node.send_command(
            f'export SGE_ROOT={SGE_ROOT} && {QSTAT} -xml')
        return qstat_xml

    def _parse_qstat(self, qstat_output) -> Tuple[int, str]:
        '''
        Parse the output of the qstat -xml command

        '''
        root = ET.fromstring(qstat_output)
        jobs_queue: Tuple[int, str] = []
        for job_list in root.findall('.//job_list'):
            job_id = job_list.find('JB_job_number').text
            current_job_state = job_list.find('state').text
            jobs_queue.append((int(job_id), current_job_state))
        return jobs_queue

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
