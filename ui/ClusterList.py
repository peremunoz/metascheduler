from typing import List
import inquirer
from utils.CSV_Helper import read_csv

CLUSTER_IMPLEMENTATION_FILE = "./data/supported_clusters.csv"

def get_cluster_list() -> List[str]:
    """
    Gets the list of implemented clusters systems.

    """
    cluster_list = read_csv(CLUSTER_IMPLEMENTATION_FILE)
    return cluster_list

def ask_for_cluster() -> str:
    """
    Asks the user to select a cluster system.

    """
    questions = [
        inquirer.List('cluster_system',
                        message="Select a cluster system",
                        choices=get_cluster_list(),
                    ),
    ]

    answers = inquirer.prompt(questions)
    return answers['cluster_system']