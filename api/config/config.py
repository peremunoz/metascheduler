import os
import json
from pathlib import Path
from typing import Any, List
from api.utils.DatabaseHelper import DatabaseHelper
from api.interfaces.Scheduler import Scheduler
from api.utils.SchedulerFactory import get_scheduler
from api.utils.Singleton import Singleton
from api.interfaces.Node import Node


class AppConfig(metaclass=Singleton):

    _config: Any
    root: bool
    nodes: List[Node]
    master_node: Node
    schedulers: List[Scheduler]

    def __init__(self, config_file: Path = None, database_file: Path = None) -> None:
        if (os.environ.get('TESTING') == 'true'):
            config_file = Path("./config/test.config")
        if (config_file):
            self.root = os.geteuid() == 0
            self._load_config(config_file)
            self._load_nodes()
            self._load_schedulers()
            self._init_db(database_file)
        else:
            raise Exception(
                "Config file not provided on first initialization.")

    def _load_config(self, config_file: Path):
        self._config = json.loads(config_file.read_text())

    def _load_nodes(self) -> None:
        nodes = self._config['cluster']['nodes']
        nodes_list: List[Node] = []
        node_id = 0
        for node in nodes:
            node_obj = Node(node_id, node['ip'], node['port'])
            nodes_list.append(node_obj)
            node_id += 1
        self.nodes = nodes_list
        self.master_node = nodes_list[0]

    def _load_schedulers(self) -> None:
        schedulers = self._config['cluster']['schedulers']
        schedulers_list: List[Scheduler] = []
        for scheduler in schedulers:
            scheduler_obj = get_scheduler(scheduler['name'])
            schedulers_list.append(scheduler_obj)
        self.schedulers = schedulers_list

    def _init_db(self, database_file: Path) -> None:
        DatabaseHelper(self.schedulers, database_file)
