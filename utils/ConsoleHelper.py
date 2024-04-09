from rich.console import Console
from rich.text import Text

from interfaces.Cluster import Cluster

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

def print_cluster_selection(cluster: Cluster) -> None:
    """
    Prints the selected cluster.

    """
    print("Selected cluster system: ", end='')
    print_color(cluster.__str__(), "blue")

def print_scheduler_selection(cluster: Cluster) -> None:
    """
    Prints the selected schedulers.
    
    """
    print("Selected schedulers: ", end='')
    for i, scheduler in enumerate(cluster.get_schedulers()):
        if i == len(cluster.get_schedulers()) - 1:
            print_color(scheduler.__str__(), "blue", '')
            print()
        else:
            print_color(scheduler.__str__(), "blue", ', ')