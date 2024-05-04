import threading
import time
from api.utils.singleton import Singleton


class JobMonitorDaemon(metaclass=Singleton):
    def __init__(self):
        self._stop_event = threading.Event()

    def start(self):
        while not self._stop_event.is_set():
            print(
                f'Job Monitor Daemon is running... pid: {threading.get_ident()}')
            self._monitor_jobs()
            self._check_queues()
            self._make_decisions()
            time.sleep(5)

    def stop(self):
        print(f'Stopping Job Monitor Daemon... pid: {threading.get_ident()}')
        self._stop_event.set()

    def _monitor_jobs(self):
        print('Monitoring jobs...')
        pass

    def _check_queues(self):
        print('Checking queues...')
        pass

    def _make_decisions(self):
        print('Making decisions...')
        pass
