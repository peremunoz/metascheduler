from typing import List
import inquirer
from utils.CSV_Helper import read_csv

SCHEDULER_IMPLEMENTATION_FILE = "./data/supported_schedulers.csv"

def get_schedulers_choices() -> List[str]:
    """
    Gets the list of implemented schedulers.

    """
    scheduler_list = read_csv(SCHEDULER_IMPLEMENTATION_FILE)
    return scheduler_list

def ask_for_schedulers() -> List[str]:
    """
    Asks the user to select the schedulers.

    """
    questions = [
        inquirer.Checkbox('schedulers',
                        message="Select the schedulers (use the right/left arrows)",
                        choices=get_schedulers_choices(),
                    ),
    ]

    answers = inquirer.prompt(questions)
    return answers['schedulers']