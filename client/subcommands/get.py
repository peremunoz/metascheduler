from requests import Response
import typer
from rich import print, print_json
from rich.panel import Panel

from client.helpers.http_client import HTTP_Client

app = typer.Typer(no_args_is_help=True)


@app.command()
def cluster_mode():
    response: Response = HTTP_Client().get('/cluster/mode')
    cluster_mode = response.json()
    panel = Panel(
        f"[bold cyan]Cluster Mode:[/bold cyan]\n{cluster_mode}",
        title="[bold magenta]Cluster Information[/bold magenta]",
        border_style="green"
    )
    print(panel)


if __name__ == "__main__":
    app()
