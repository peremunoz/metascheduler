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


@app.command(help="Edit the cluster working mode.")
def cluster_mode(cluster_mode: Annotated[ClusterMode, typer.Argument(help="The cluster mode to set the cluster to.", callback=lambda x: x.lower(), case_sensitive=False)]):
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


@app.command(help="Edit a job.")
def job(job_id: Annotated[int, typer.Argument(help="The Job ID to edit.")],
        queue: Annotated[int, typer.Option(
            help="The queue id to set the job to.")] = None,
        name: Annotated[str, typer.Option(
            help="The name to set the job to.")] = None,
        path: Annotated[str, typer.Option(
            help="The path to set the job to.")] = None,
        options: Annotated[str, typer.Option(help="The options to set the job to.")] = ''):
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
