from typing import List, Tuple
from api.constants.job_status import JobStatus
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler
from api.routers.jobs import update_job_status
import re

HADOOP_HOME = '/opt/hadoop'
JAVA_HOME = '/usr/lib/jvm/jre/'

# export JAVA_HOME=/usr/lib/jvm/jre/ && /opt/hadoop/bin/yarn jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 2 4


class ApacheHadoop(Scheduler):
    '''
    Apache Hadoop Scheduler

    '''

    def __init__(self) -> None:
        super().__init__()
        self.name = 'Apache Hadoop'

    def __str__(self) -> str:
        return f'Apache Hadoop Scheduler: {self.master_node.ip}:{self.master_node.port}'

    def update_job_list(self, metascheduler_queue: List[Job]):
        '''
        Update the job list.
        Also update the job status in the database.

        As Apache Hadoop does not have a scheduler, this method is not implemented.

        '''
        if not self.running_jobs:
            return
        response = self._call_yarn_application()
        if not self._is_any_job_running(response):
            for job in self.running_jobs:
                update_job_status(job.id_, job.owner, JobStatus.COMPLETED)
                self._reset_java_process_nice()
            self.running_jobs = []

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
        if self.running_jobs:
            print('There is already a job running. Only one job can run at a time.')
            return
        try:
            self._call_yarn_jar(job)
            self.running_jobs.append(job)
            update_job_status(job.id_, job.owner, JobStatus.RUNNING)
        except Exception as e:
            print(f'Error: {e}')
            update_job_status(job.id_, job.owner, JobStatus.ERROR)

    def _call_yarn_jar(self, job: Job):
        '''
        Call the yarn jar command to run the job.

        '''
        self.master_node.send_command_async(
            f'{HADOOP_HOME}/bin/yarn jar {job.path} {job.options}'
        )
        # self.master_node.send_command_async(
        #     f'export JAVA_HOME={JAVA_HOME} && {HADOOP_HOME}/bin/yarn jar hadoop-mapreduce-examples-3.3.6.jar pi 2 4 &'
        # )

    def _call_yarn_application(self) -> str:
        '''
        Call the yarn application -list command to get the list of running jobs.

        '''
        response = self.master_node.send_command(
            f'export JAVA_HOME={JAVA_HOME} && {HADOOP_HOME}/bin/yarn application -list'
        )
        return response

    def _is_any_job_running(self, response: str) -> bool:
        '''
        Check if any job is running, parsing the response from the yarn application -list command.

        '''
        match = re.search(r"Total number of applications.*:\s*(\d+)", response)
        if match:
            return int(match.group(1)) > 0
        return False

    def adjust_nice_of_all_jobs(self, new_nice: int):
        for node in self.nodes:
            ps_output = node.send_command(f'ps -eo pid,comm,nice')
            job_processes_pid_nice: Tuple[int, int] = self._get_job_processes_from_ps(
                ps_output)
            for pid, actual_nice in job_processes_pid_nice:
                if actual_nice == new_nice:
                    continue
                node.send_command(f'renice {new_nice} {pid}')

    def get_all_jobs_info(self) -> List[Tuple[int, int, float, float]]:
        '''
        Get the information of all running jobs

        '''
        node = self.master_node
        ps_output = node.send_command(f'ps -eo pid,comm,nice,%cpu,%mem')
        return self._get_job_info_from_ps(ps_output)

    def _get_job_info_from_ps(self, ps_output: str) -> List[Tuple[int, int, float, float]]:
        '''
        Get the list of processes of the running jobs.

        Search for the sge_shepherd process and get the PID of the process and the nice value.

        '''
        job_processes_pid_nice_cpu_mem = []
        lines = ps_output.split('\n')
        for line in lines:
            if 'java' in line:
                job_processes_pid_nice_cpu_mem.append(
                    (int(line.split()[0]), int(line.split()[2]), float(line.split()[3]), float(line.split()[4])))
        return job_processes_pid_nice_cpu_mem

    def _get_job_processes_from_ps(self, ps_output: str) -> Tuple[int, int]:
        job_processes_pid_nice = []
        lines = ps_output.split('\n')
        for line in lines:
            if 'java' in line:
                job_processes_pid_nice.append(
                    (int(line.split()[0]), int(line.split()[2])))
        return job_processes_pid_nice

    def _reset_java_process_nice(self):
        for node in self.nodes:
            ps_output = node.send_command(f'ps -eo pid,comm,nice')
            job_processes_pid_nice: Tuple[int, int] = self._get_job_processes_from_ps(
                ps_output)
            for pid, actual_nice in job_processes_pid_nice:
                if actual_nice == 0:
                    continue
                node.send_command(f'renice 0 {pid}')
