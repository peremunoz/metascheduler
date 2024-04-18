from typing import List, Tuple
from rich.table import Table
from rich.console import Console
from utils.CSV_Helper import read_csv

SUPPORTED_SCHEDULERS_CSV = "./data/supported_schedulers.csv"

def get_scheduler_options() -> List[str]:
    """
    Returns the available schedulers.

    """
    return read_csv(SUPPORTED_SCHEDULERS_CSV)

def print_available_schedulers() -> List[str]:
    """
    Prints the available schedulers, and returns list with the printed schedulers names, in order.

    """
    table = Table(title="Supported schedulers")
    table.add_column("Name", justify="center", style="cyan")
    table.add_column("Option number", justify="center", style="black")

    for i, scheduler in enumerate(get_scheduler_options()):
        table.add_row(scheduler, str(i))
    
    console = Console()
    console.print(table)

    return get_scheduler_options()