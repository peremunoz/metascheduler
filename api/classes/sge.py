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
        return f'SGE Scheduler: {self.master_node.ip}:{self.master_node.port}'

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
                actual_jobs.remove(job)
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
        Call the qsub command to queue the job
        and return the job id assigned by the scheduler.

        '''
        message = self.master_node.send_command(
            f'sudo -u {job.owner} sh -c \'export SGE_ROOT={SGE_ROOT} && cd {job.pwd} && {QSUB} -N {job.name} -o {job.pwd} -e {job.pwd} {job.path} {job.options}\'')
        assigned_job_id = self._parse_qsub(message)
        return assigned_job_id

    def _parse_qsub(self, qsub_output) -> int:
        '''
        Parse the output of the qsub command

        '''
        return int(qsub_output.split()[2])

    def get_all_jobs_info(self) -> List[Tuple[int, int, float, float, str]]:
        '''
        Get the information of all running jobs

        '''
        node = self.master_node
        ps_output = node.send_command(
            f'ps -eo pid,comm,nice,%cpu,%mem,ppid,user')
        return self._get_job_info_from_ps(ps_output)

    def adjust_nice_of_all_jobs(self, new_nice: int):
        '''
        Adjust the nice value of all running jobs' processes.

        '''
        for node in self.nodes:
            ps_output = node.send_command(f'ps -eo pid,comm,nice,ppid,user')
            job_processes_pid_nice: Tuple[int, int, str] = self._get_job_processes_from_ps(
                ps_output)
            for pid, actual_nice, user in job_processes_pid_nice:
                if actual_nice == new_nice:
                    continue
                node.send_command(
                    f'sudo -u {user} sh -c \'renice {new_nice} {pid}\'', critical=False)

    def adjust_nice_of_job(self, job_pid: int, new_nice: int, user: str):
        '''
        Adjust the nice value of a running job.

        '''
        for node in self.nodes:
            node.send_command(
                f'sudo -u {user} sh -c \'renice {new_nice} {job_pid}\'', critical=False)

    def _get_job_info_from_ps(self, ps_output: str) -> List[Tuple[int, int, float, float, str]]:
        '''
        Get the list of processes of the running jobs.

        Search for the sge_shepherd process and get the PID of the process and the nice value.

        '''
        job_processes_pid_nice_cpu_mem = []
        sge_executors = []
        lines = ps_output.split('\n')[1:]
        for line in lines:
            if 'sge_shepherd' in line:
                sge_executors.append(int(line.split()[0]))
        if not sge_executors:
            return job_processes_pid_nice_cpu_mem
        for line in lines:
            if not line:
                continue
            if int(line.split()[5]) in sge_executors:
                job_processes_pid_nice_cpu_mem.append(
                    (int(line.split()[0]), int(line.split()[2]), float(line.split()[3]), float(line.split()[4]), line.split()[6]))
        return job_processes_pid_nice_cpu_mem

    def _get_job_processes_from_ps(self, ps_output: str) -> Tuple[int, int, str]:
        '''
        Get the list of processes of the running jobs.

        Search for the sge_shepherd process and get the PID of the process, the nice value and the user.

        '''
        job_processes_pid_nice = []
        sge_executors = []
        lines = ps_output.split('\n')[1:]
        for line in lines:
            if 'sge_shepherd' in line:
                sge_executors.append(int(line.split()[0]))
        if not sge_executors:
            return job_processes_pid_nice
        for line in lines:
            if not line:
                continue
            if int(line.split()[3]) in sge_executors:
                job_processes_pid_nice.append(
                    (int(line.split()[0]), int(line.split()[2]), line.split()[4]))
        return job_processes_pid_nice
