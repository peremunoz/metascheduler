import json
from pathlib import Path
from typing import Any, List
from utils.Singleton import Singleton
from interfaces.Node import Node


class AppConfig(metaclass=Singleton):

    _config: Any
    nodes: List[Node]
    master_node: Node

    def __init__(self, config_file: Path = None) -> None:
        if (config_file):
            self._load_config(config_file)
            self._load_nodes()
        else:
            raise Exception(
                "Config file not provided on first initialization.")

    def _load_config(self, config_file: Path):
        self._config = json.loads(config_file.read_text())

    def _load_nodes(self) -> None:
        nodes = self._config['cluster']['nodes']
        nodes_list: List[Node] = []
        for node in nodes:
            node_obj = Node(node['ip'], node['port'],
                            node['user'], node['password'])
            nodes_list.append(node_obj)
        self.nodes = nodes_list
        self.master_node = nodes_list[0]
