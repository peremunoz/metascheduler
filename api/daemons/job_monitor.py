import threading
from time import sleep
from typing import List
from api.config.config import AppConfig
from api.interfaces.job import Job
from api.interfaces.scheduler import Scheduler
from api.routers.jobs import read_jobs
from api.utils.singleton import Singleton
from rich import print


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
    counter = 0

    def __init__(self):
        self._stop_event = threading.Event()

    def start(self):
        ''' Start the daemon '''
        log('Starting...')
        self.config = AppConfig()
        while not self._stop_event.is_set():
            self._update_jobs_queue()
            self._update_scheduler_queues()
            self._make_decisions()
            sleep(5)

    def stop(self):
        log(f'Shutting down...')
        self._stop_event.set()

    def _update_jobs_queue(self):
        ''' Update the jobs queue '''
        log('Monitoring jobs...')
        self.metascheduler_queue = read_jobs(
            owner='root', status=None, queue=None)
        log(f'Jobs in queue: {len(self.metascheduler_queue)}')
        pass

    def _update_scheduler_queues(self):
        ''' Update the scheduler queues '''
        log('Checking queues...')
        for scheduler in self.config.schedulers:
            scheduler.update_job_list()
            log(f'{scheduler.name}: {len(scheduler.get_job_list())} jobs')
        pass

    def _make_decisions(self):
        ''' Make decisions based on the monitored jobs and queues '''
        log('Making decisions...')
        if (self.counter == 1):
            scheduler = self.config.schedulers[0]
            scheduler.queue_job(self.metascheduler_queue[0])
            log(
                f'Queued job {self.metascheduler_queue[0].name} to {scheduler.name}')
        if (self.counter == 2):
            scheduler = self.config.schedulers[0]
            scheduler.queue_job(self.metascheduler_queue[1])
            log(
                f'Queued job {self.metascheduler_queue[1].name} to {scheduler.name}')
        self.counter += 1
        pass
