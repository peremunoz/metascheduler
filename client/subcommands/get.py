from dataclasses import dataclass
from typing_extensions import Annotated
from requests import Response
import typer
from rich import print, print_json
from rich.panel import Panel
from rich.table import Table

from client.helpers.http_client import HTTP_Client

app = typer.Typer(no_args_is_help=True)


@dataclass
class NodeResponse:
    id: int
    ip: str
    port: int
    is_alive: bool


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


@app.command()
def nodes():
    response: Response = HTTP_Client().get('/cluster/nodes')
    nodes_raw = response.json()
    nodes = [NodeResponse(**node) for node in nodes_raw]
    table = Table(title="Cluster Nodes", show_header=True,
                  header_style="bold magenta")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("IP", style="dim")
    table.add_column("Port", style="dim")
    table.add_column("Is Alive", style="dim")

    for node in nodes:
        table.add_row(str(node.id), node.ip, str(
            node.port), str(node.is_alive))

    panel = Panel(table, border_style="green")
    print(panel)


@app.command()
def master_node():
    response: Response = HTTP_Client().get('/cluster/nodes/master')
    master_node = NodeResponse(**response.json())
    table = Table(title="Master Node", show_header=True,
                  header_style="bold magenta")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("IP", style="dim")
    table.add_column("Port", style="dim")
    table.add_column("Is Alive", style="dim")

    table.add_row(str(master_node.id), master_node.ip, str(
        master_node.port), str(master_node.is_alive))

    panel = Panel(table, border_style="green")
    print(panel)


@app.command()
def node(node_id: Annotated[int, typer.Argument(help="Node ID")]):
    response: Response = HTTP_Client().get(f'/cluster/nodes/{node_id}')
    node = NodeResponse(**response.json())
    table = Table(title="Node", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("IP", style="dim")
    table.add_column("Port", style="dim")
    table.add_column("Is Alive", style="dim")

    table.add_row(str(node.id), node.ip, str(node.port), str(node.is_alive))

    panel = Panel(table, border_style="green")
    print(panel)


@app.command()
def queues():
    response: Response = HTTP_Client().get('/queues')
    queues = response.json()
    table = Table(title="Queues", show_header=True,
                  header_style="bold magenta")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("Scheduler Name", style="dim")

    for queue in queues:
        table.add_row(str(queue['id']), queue['scheduler_name'])

    panel = Panel(table, border_style="green")
    print(panel)


if __name__ == "__main__":
    app()
