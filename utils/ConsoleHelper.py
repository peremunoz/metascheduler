from rich.console import Console
from rich.text import Text

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