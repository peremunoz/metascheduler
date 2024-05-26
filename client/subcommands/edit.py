from enum import Enum
import os
from typing_extensions import Annotated
from requests import Response
import typer
from rich import print
from rich.panel import Panel

from client.helpers.http_client import HTTP_Client

app = typer.Typer(no_args_is_help=True)


class ClusterMode(str, Enum):
    EXCLUSIVE = 'exclusive',
    BEST_EFFORT = 'best_effort',
    SHARED = 'shared',
    DYNAMIC = 'dynamic'


@app.command()
def cluster_mode(cluster_mode: Annotated[ClusterMode, typer.Argument(help="Cluster mode", callback=lambda x: x.lower(), case_sensitive=False)]):
    request_data = {
        "user": os.getenv("USER"),
        "mode": cluster_mode
    }
    response: Response = HTTP_Client().put('/cluster/mode', request_data)
    respose_message = response.json()["message"] + f" ({cluster_mode})"
    panel = Panel(
        f"[bold cyan]Response:[/bold cyan]\n{respose_message}",
        title="[bold magenta]Set Cluster Mode[/bold magenta]",
        border_style="green"
    )
    print(panel)


if __name__ == "__main__":
    app()
