from client.helpers.singleton import Singleton
import requests
from rich import print
from rich.console import Console
from rich.panel import Panel


class HTTP_Client(metaclass=Singleton):
    def __init__(self, url, port):
        self.url = url
        self.port = port
        self.console = Console()

    def handle_request_error(self, e: requests.exceptions.RequestException):
        if isinstance(e, requests.exceptions.ConnectionError):
            error_message = (
                "[bold red]Error: Connection refused[/bold red]\n"
                "[yellow]Possible reasons:[/yellow]\n"
                "- The server is not running.\n"
                "- The URL or port is incorrect.\n"
                "[cyan]Suggestion:[/cyan] Please check the server status and ensure the correct URL and port are specified."
            )
        elif isinstance(e, requests.exceptions.Timeout):
            error_message = (
                "[bold red]Error: Timeout[/bold red]\n"
                "[yellow]Possible reasons:[/yellow]\n"
                "- The server is taking too long to respond.\n"
                "- The server might be overloaded or down.\n"
                "[cyan]Suggestion:[/cyan] Try again later or check the server status."
            )
        else:
            error_message = (
                "[bold red]Error: Request exception[/bold red]\n"
                "[yellow]Possible reasons:[/yellow]\n"
                "- An unexpected error occurred.\n"
                "[cyan]Suggestion:[/cyan] Check the request and try again."
            )
        panel = Panel(
            error_message, title="[bold red]Request Error[/bold red]", border_style="red")
        self.console.print(panel)
        exit(1)

    def get(self, endpoint):
        try:
            response = requests.get(
                f'http://{self.url}:{self.port}/{endpoint}')
            if response.status_code == 200:
                return response
            else:
                self.console.print(
                    f"[bold red]Error: {response.status_code}[/bold red]\n"
                    f"[yellow]Response message:[/yellow] {response.text}\n"
                    f"[cyan]Suggestion:[/cyan] Check the request and try again."
                )
        except requests.exceptions.RequestException as e:
            self.handle_request_error(e)
