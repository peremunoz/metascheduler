from typing import List
from pathlib import Path
import json

import typer
from interfaces.Scheduler import Scheduler
from interfaces.Node import Node
from ui.AvailableSchedulers import print_available_schedulers
from utils.ConsoleHelper import print_node_setup, print_scheduler_setup
from utils.SchedulerFactory import get_scheduler


class Cluster:
    """
    Interface for a cluster.

    """
    master: Node
    nodes: List[Node]
    schedulers: List[Scheduler]

    def setup_from_file(self, file_path: Path):
        """
        Sets up the cluster from a file.

        """
        json_config = json.loads(file_path.read_text())

        nodes = json_config['cluster']['nodes']
        nodes_list = []
        for node in nodes:
            nodes_list.append(Node(node['ip'], node['port'], node['user'], node['password']))
        self._set_nodes(nodes_list)

        schedulers = json_config['cluster']['schedulers']
        schedulers_list = []
        for scheduler in schedulers:
            schedulers_list.append(get_scheduler(scheduler['name']))
        self._set_schedulers(schedulers_list)

        print_node_setup(self)
        print()
        print_scheduler_setup(self)

    def manual_setup(self):
        """
        Sets up the cluster manually, via the console.

        """
        self._setup_schedulers()
        self._setup_nodes()
    
    def _setup_schedulers(self):
        """
        Sets up the schedulers of the cluster.
        
        """
        all_scheduler_names_str: List[str] = print_available_schedulers()
        schedulers_selected_options: List[int] = typer.prompt("Enter the options of the schedulers you want to use, separated by commas: ").split(",")
        scheduler_names_str: List[str] = []
        for option in schedulers_selected_options:
            scheduler_names_str.append(all_scheduler_names_str[int(option)])
        schedulers_list: List[Scheduler] = []
        for scheduler in scheduler_names_str:
            schedulers_list.append(get_scheduler(scheduler))
        self.set_schedulers(schedulers_list)
        print_scheduler_setup(self)

    def _setup_nodes(self):
        """
        Sets up the nodes of the cluster.
        
        """
        nodes_number: int = int(input("Enter the number of nodes: "))
        nodes_list: List[Node] = []
        for i in range(nodes_number):
            ssh_ip: str = input(f"Enter the IP of node {i + 1}: ").strip()
            ssh_port: str = input(f"Enter the port of node {i + 1} [22]: ").strip()
            if ssh_port == "":
                ssh_port = 22
            ssh_user: str = input(f"Enter the user of node {i + 1} [root]: ").strip()
            if ssh_user == "":
                ssh_user = "root"
            ssh_password: str = input(f"Enter the password of node {i + 1} [root]: ").strip()
            if ssh_password == "":
                ssh_password = "root"
            nodes_list.append(Node(ssh_ip, int(ssh_port), ssh_user, ssh_password))
        self._set_nodes(nodes_list)
        print_node_setup(self)
    
    def connect(self):
        """
        Connects to the cluster.
        
        """
        raise NotImplementedError("Method not implemented")
    
    def disconnect(self):
        """
        Disconnects from the cluster.
        
        """
        raise NotImplementedError("Method not implemented")
    
    def is_active(self) -> bool:
        """
        Checks if the cluster is active.
        
        """
        raise NotImplementedError("Method not implemented")
    
    def __str__(self):
        """
        String representation of the cluster.

        """
        raise NotImplementedError("Method not implemented")
    
    def get_schedulers(self):
        """
        Gets the schedulers of the cluster.
        
        """
        return self.schedulers
    
    def _set_schedulers(self, schedulers: List[Scheduler]):
        """
        Sets the schedulers of the cluster.
        
        """
        self.schedulers = schedulers
    
    def get_nodes(self) -> List[Node]:
        """
        Gets the nodes of the cluster.
        
        """
        return self.nodes
    
    def _set_nodes(self, nodes: List[Node]):
        """
        Sets the nodes of the cluster.
        
        """
        self.nodes = nodes
    
    def get_master(self) -> Node:
        """
        Gets the master node of the cluster.
        
        """
        return self.master
    
    def _set_master(self, master: Node):
        """
        Sets the master node of the cluster.
        
        """
        self.master = master
