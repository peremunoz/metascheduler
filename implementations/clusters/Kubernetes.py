from typing import List

from interfaces.Cluster import Cluster
from interfaces.Scheduler import Scheduler
from ui.KubeConfigPath import ask_for_kube_config_path
from ui.NodeList import ask_for_master_node
from ui.SchedulersCheckbox import ask_for_schedulers
from utils.ConsoleHelper import print_scheduler_selection, successful_cluster_setup, successful_scheduler_setup
from utils.SchedulerFactory import get_scheduler
from kubernetes import config, client


class Kubernetes(Cluster):

    def setup(self):
        """
        Sets up the Kubernetes cluster.

        """
        kube_config_path: str = ask_for_kube_config_path()
        if kube_config_path == "":
            config.load_kube_config()
        else:
            config.load_kube_config(kube_config_path)
        successful_cluster_setup(self)

    def setup_schedulers(self):
        """
        Sets up the schedulers of the Kubernetes cluster.

        """
        schedulers_str: List[str] = ask_for_schedulers()
        schedulers_list: List[Scheduler] = []
        for scheduler in schedulers_str:
            schedulers_list.append(get_scheduler(scheduler))
        self.set_schedulers(schedulers_list)
        print_scheduler_selection(self)

        # For each scheduler, define the master node
        pods_name = self.get_pods_name()
        for scheduler in self.get_schedulers():
            scheduler_master_node = ask_for_master_node(scheduler, pods_name)
            scheduler.set_master(scheduler_master_node)
            successful_scheduler_setup(scheduler)


    def get_pods_name(self, namespace: str = 'default'):
        """
        Prints the list of pods in the cluster.

        """
        v1 = client.CoreV1Api()
        pod_list = v1.list_namespaced_pod(namespace)
        pods = []
        for i in pod_list.items:
            pods.append(i.metadata.name)
        return pods

    def __str__(self):
        return "Kubernetes"