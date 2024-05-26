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


@app.command()
def job(job_id: Annotated[int, typer.Argument(help="Job ID")],
        queue: Annotated[int, typer.Option(help="Job queue")] = None,
        name: Annotated[str, typer.Option(help="Job name")] = None,
        path: Annotated[str, typer.Option(help="Job path")] = None,
        options: Annotated[str, typer.Option(help="Job options")] = ''):
    params = {
        "owner": os.getenv("USER")
    }
    body = {}
    if queue:
        body["queue"] = queue
    if name:
        body["name"] = name
    if path:
        body["path"] = path
    if options:
        body["options"] = options
    if body == {}:
        print("No changes were made.")
        exit(0)
    response: Response = HTTP_Client().put(f'/jobs/{job_id}', body, params)
    response_message = response.json()["message"]
    panel = Panel(
        f"[bold cyan]Response:[/bold cyan]\n{response_message}",
        title="[bold magenta]Delete Job[/bold magenta]",
        border_style="green"
    )
    print(panel)


if __name__ == "__main__":
    app()
