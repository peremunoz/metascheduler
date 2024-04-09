from rich.console import Console
from rich.text import Text

from interfaces.Cluster import Cluster
from interfaces.Scheduler import Scheduler

def print_color(text: str, color: str, end='\n') -> None:
    """
    Prints the given text with the given color.

    """
    console = Console()
    console.print(Text(text, style=f"bold {color}"), end=end)

def clear_console() -> None:
    """
    Clears the console.

    """
    console = Console()
    console.clear()

def print_cluster_selection(cluster: Cluster, color="blue") -> None:
    """
    Prints the selected cluster.

    """
    print("Selected cluster system: ", end='')
    print_color(cluster.__str__(), color)

def print_scheduler_selection(cluster: Cluster, color="blue") -> None:
    """
    Prints the selected schedulers.
    
    """
    print("Selected schedulers: ", end='')
    for i, scheduler in enumerate(cluster.get_schedulers()):
        if i == len(cluster.get_schedulers()) - 1:
            print_color(scheduler.__str__(), color, '')
            print()
        else:
            print_color(scheduler.__str__(), color, ', ')

def successful_cluster_setup(cluster: Cluster) -> None:
    """
    Prints a success message for the cluster setup.

    """
    print_color(f"Successfully set up the {cluster.__str__()} cluster!", "green")

def successful_scheduler_setup(scheduler: Scheduler) -> None:
    """
    Prints a success message for the scheduler setup.

    """
    print_color(f"Successfully set up the {scheduler.__str__()} scheduler!", "green")