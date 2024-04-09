from typing import List
import inquirer

from interfaces.Scheduler import Scheduler

def ask_for_master_node(scheduler: Scheduler, node_list: List[str]) -> str:
    """
    Asks the user to select a master node.

    """
    questions = [
        inquirer.List('master_node',
                        message=f"Select the master node for {scheduler.__str__()}",
                        choices=node_list,
                    ),
    ]

    answers = inquirer.prompt(questions)
    return answers['master_node']