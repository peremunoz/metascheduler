from typing import List
from interfaces.Cluster import Cluster
from interfaces.Scheduler import Scheduler
from ui.SchedulersCheckbox import ask_for_schedulers
from utils.ConsoleHelper import clear_console, print_cluster_selection, print_scheduler_selection
from utils.SchedulerFactory import get_scheduler


class Kubernetes(Cluster):

    def setup(self):
        """
        Sets up the Kubernetes cluster.

        """
        schedulers_str: List[str] = ask_for_schedulers()
        schedulers_list: List[Scheduler] = []
        for scheduler in schedulers_str:
            schedulers_list.append(get_scheduler(scheduler))
        self.set_schedulers(schedulers_list)
        clear_console()
        print_cluster_selection(self)
        print_scheduler_selection(self)

    def __str__(self):
        return "Kubernetes"