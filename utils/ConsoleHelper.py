from rich.console import Console
from rich.text import Text

#from interfaces.Cluster import Cluster
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

def print_scheduler_setup(cluster, color="blue") -> None:
    """
    Prints the setup schedulers.
    
    """
    print_color("Schedulers setup: ", color="bold")
    for i, scheduler in enumerate(cluster.get_schedulers()):
        if i == len(cluster.get_schedulers()) - 1:
            print_color(scheduler.__str__(), color, '')
            print()
        else:
            print_color(scheduler.__str__(), color, ', ')

def print_node_setup(cluster, color="blue") -> None:
    """
    Prints the setup nodes.
    
    """
    print_color("Nodes setup: ", color="bold")
    for i, node in enumerate(cluster.get_nodes()):
        print_color(f"Node {i + 1}: {node}", color)