from typing import List
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
