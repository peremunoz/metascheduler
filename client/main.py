import ipaddress
import os
from typing_extensions import Annotated
import typer
from client.helpers.http_client import HTTP_Client
import client.subcommands.get as get

app = typer.Typer(no_args_is_help=True)
app.add_typer(get.app, name='get')


def validate_ip(ip: str) -> str:
    if ip == "localhost":
        return "0.0.0.0"
    try:
        ipaddress.ip_address(ip)
        return ip
    except ValueError:
        raise typer.BadParameter(f"Invalid IP address: {ip}")


@app.callback()
def callback(
    ip: Annotated[str, typer.Option(
        help="IP where the API is running",
        show_default=True,
        callback=validate_ip,
        envvar="API_IP",
    )] = "0.0.0.0",
    port: Annotated[int, typer.Option(
        help="Port where the API is running",
        show_default=True,
        envvar="API_PORT",
    )] = 8000,
):
    HTTP_Client(ip, port)
    os.environ["API_IP"] = ip
    os.environ["API_PORT"] = str(port)


if __name__ == "__main__":
    app()
