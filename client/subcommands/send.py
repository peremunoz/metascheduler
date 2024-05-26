import os
from typing_extensions import Annotated
import typer
from rich import print
from rich.panel import Panel

from client.helpers.http_client import HTTP_Client

app = typer.Typer(no_args_is_help=True)


@app.command(help="Send a job to the metascheduler.")
def job(name: Annotated[str, typer.Option(help="Job name.")],
        queue: Annotated[int, typer.Option(help="Job queue.")],
        path: Annotated[str, typer.Option(help="Job path.")],
        options: Annotated[str, typer.Option(help="Job options.")] = ''):
    request_data = {
        "name": name,
        "queue": queue,
        "owner": os.getenv("USER"),
        "path": path,
        "options": options
    }
    response = HTTP_Client().post('/jobs', request_data)
    response_message = response.json()["message"]
    panel = Panel(
        f"[bold cyan]Response:[/bold cyan]\n{response_message}",
        title="[bold magenta]Create Job[/bold magenta]",
        border_style="green"
    )
    print(panel)
