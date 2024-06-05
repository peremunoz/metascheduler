import threading
from time import sleep
from typing import List
from api.config.config import AppConfig
from api.constants.job_status import JobStatus
from api.daemons.policies.planification_policy import PlanificationPolicy
from api.interfaces.job import Job
from api.routers.jobs import read_jobs
from api.utils.policy_factory import get_policy_by_name
from api.utils.singleton import Singleton
from rich import print

CYCLE_TIME = 5


def log(message):
    ''' Log messages to the console '''
    prefix = 'DAEMON:'.ljust(10)
    print(f'[cyan]{prefix}[/cyan]{message}')


class JobMonitorDaemon(metaclass=Singleton):
    ''' The Job Monitor Daemon is responsible for monitoring the jobs in the database,
    checking the scheduler queues, and making decisions based on the monitored jobs and queues.

    The daemon runs in a separate thread and is started and stopped by the main application.

    The Job Monitor Daemon is a Singleton class, meaning that only one instance of the class
    can be created. This is useful because we only need one instance of the daemon running
    in the application.
    '''

    config: AppConfig
    metascheduler_queue: List[Job] = []
    to_be_queued_jobs: List[Job] = []
    counter = 0
    planification_policy: PlanificationPolicy = None

    def __init__(self):
        self._stop_event = threading.Event()

    def start(self):
        ''' Start the daemon '''
        log('Starting...')
        self.config = AppConfig()
        while not self._stop_event.is_set():
            self._execute_cycle()
            sleep(CYCLE_TIME)

    def stop(self):
        log(f'Shutting down...')
        self._stop_event.set()

    def _execute_cycle(self):
        self.planification_policy = get_policy_by_name(
            self.config.get_mode(), PlanificationPolicy(self.config.schedulers, self.config.get_highest_priority()))
        self._update_jobs_queue()
        self._update_scheduler_queues()
        self._make_decisions()

    def _update_jobs_queue(self):
        ''' Update the jobs queue '''
        log('Monitoring jobs...')
        self.metascheduler_queue = read_jobs(
            owner='root', status=None, queue=None)
        self.to_be_queued_jobs = read_jobs(
            owner='root', status=JobStatus.TO_BE_QUEUED, queue=None)
        log(f'Jobs in all queue: {len(self.metascheduler_queue)}')
        log(f'Jobs to be queued: {len(self.to_be_queued_jobs)}')
        pass

    def _update_scheduler_queues(self):
        ''' Update the scheduler queues '''
        log('Checking queues...')
        for scheduler in self.config.schedulers:
            scheduler.update_job_list(
                self.metascheduler_queue)
            log(f'{scheduler.name}: {len(scheduler.get_job_list())} jobs')
        pass

    def _make_decisions(self):
        ''' Make decisions based on the monitored jobs and queues '''
        log('Making decisions...')
        self.planification_policy.apply(self.to_be_queued_jobs)
        pass
