from typing import List, Tuple
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

    _last_job_list_id: List[int] = []

    def __init__(self) -> None:
        super().__init__()
        self.name = 'SGE'

    def __str__(self) -> str:
        return f'SGE Scheduler: {self.hostname}:{self.port}'

    def update_job_list(self, metascheduler_queue: List[Job]):
        '''
        Update the internal job list.
        Also update the job status in the database.

        '''

        qstat = self._call_qstat()
        jobs_id_state: Tuple[str, int] = self._parse_qstat(qstat)
        actual_jobs: List[Job] = []
        for job_id_state in jobs_id_state:
            job = next(
                (job for job in metascheduler_queue if job.scheduler_job_id == job_id_state[0]), None)
            if job is None:
                continue
            actual_jobs.append(job)
            if job_id_state[1] == 'qw':
                update_job_status(job.id_, job.owner, JobStatus.QUEUED)
            if job_id_state[1] == 'Eqw':
                update_job_status(job.id_, job.owner, JobStatus.ERROR)
            if job_id_state[1] == 'r':
                update_job_status(job.id_, job.owner, JobStatus.RUNNING)
        ended_jobs_id = [
            job_id for job_id in self._last_job_list_id if job_id not in [job.scheduler_job_id for job in actual_jobs]]
        ended_jobs = [
            job for job in metascheduler_queue if job.scheduler_job_id in ended_jobs_id]
        for job in ended_jobs:
            update_job_status(job.id_, job.owner, JobStatus.COMPLETED)
        self.running_jobs = actual_jobs
        self._last_job_list_id = [job.scheduler_job_id for job in actual_jobs]

    def get_job_list(self) -> List[Job]:
        '''
        Get the list of jobs from the SGE scheduler

        '''
        return self.running_jobs

    def _call_qstat(self) -> str:
        '''
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
        try:
            sge_job_id = self._call_qsub(job)
            set_job_scheduler_job_id(job.id_, job.owner, sge_job_id)
            update_job_status(job.id_, job.owner, JobStatus.QUEUED)
            self.running_jobs.append(job)
        except Exception as e:
            raise e

    def _call_qsub(self, job: Job) -> int:
        '''
        TODO:
        Call the qsub command to queue the job
        and return the job id assigned by the scheduler.

        '''
        script_path = job.pwd + '/' + job.path
        message = self.master_node.send_command(
            f'export SGE_ROOT={SGE_ROOT} && {QSUB} -N {job.name} -o {script_path} -e {script_path} {script_path} {job.options}')
        assigned_job_id = self._parse_qsub(message)
        return assigned_job_id

    def _parse_qsub(self, qsub_output) -> int:
        '''
        Parse the output of the qsub command

        '''
        return int(qsub_output.split()[2])
