from enum import Enum
import os
from typing_extensions import Annotated
from requests import Response
import typer
from rich import print
from rich.panel import Panel

from client.helpers.http_client import HTTP_Client

app = typer.Typer(no_args_is_help=True)


@app.command()
def job(job_id: Annotated[int, typer.Argument(help="Job ID")]):
    params = {
        "owner": os.getenv("USER")
    }
    response: Response = HTTP_Client().delete(f'/jobs/{job_id}', params=params)
    response_message = response.json()["message"]
    panel = Panel(
        f"[bold cyan]Response:[/bold cyan]\n{response_message}",
        title="[bold magenta]Delete Job[/bold magenta]",
        border_style="green"
    )
    print(panel)


if __name__ == "__main__":
    app()
