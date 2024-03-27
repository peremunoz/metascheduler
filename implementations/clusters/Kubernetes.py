from typing import List
from interfaces.Cluster import Cluster
from interfaces.Scheduler import Scheduler
from ui.SchedulersCheckbox import ask_for_schedulers
from utils.ColorPrinter import print_color
from utils.SchedulerFactory import get_scheduler


class KubernetesCluster(Cluster):

    def setup(self):
        """
        Sets up the Kubernetes cluster.

        """
        schedulers_str: List[str] = ask_for_schedulers()
        print("Selected schedulers: ", end='')
        for scheduler in schedulers_str:
            print_color(scheduler, "blue", ' ')
        print()
        schedulers_list: List[Scheduler] = []
        for scheduler in schedulers_str:
            schedulers_list.append(get_scheduler(scheduler))
        self.set_schedulers(schedulers_list)

    def __str__(self):
        return "Kubernetes Cluster with schedulers: " + ', '.join([str(scheduler) for scheduler in self.schedulers])