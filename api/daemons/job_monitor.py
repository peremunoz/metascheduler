import threading
import time
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

    metascheduler_queue = []

    def __init__(self):
        self._stop_event = threading.Event()

    def start(self):
        ''' Start the daemon '''
        log('Starting...')
        while not self._stop_event.is_set():
            self._monitor_jobs()
            self._check_queues()
            self._make_decisions()
            time.sleep(5)

    def stop(self):
        log(f'Shutting down...')
        self._stop_event.set()

    def _monitor_jobs(self):
        ''' Monitor the jobs in the database '''
        log('Monitoring jobs...')
        pass

    def _check_queues(self):
        ''' Check the scheduler queues '''
        log('Checking queues...')
        pass

    def _make_decisions(self):
        ''' Make decisions based on the monitored jobs and queues '''
        log('Making decisions...')
        pass
