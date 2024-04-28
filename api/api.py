from pathlib import Path
from fastapi import FastAPI, HTTPException
import typer
from typing_extensions import Annotated
from config.config import AppConfig


app = FastAPI()


@app.get("/")
@app.get("/status")
def read_status():
    return {"status": "running", "root": AppConfig().root}


@app.get("/nodes")
def read_nodes():
    return [{"id": node.id, "ip": node.ip, "port": node.port, "ssh_user": node.ssh_user, "is_alive": node.is_alive()} for node in AppConfig().nodes]


@app.get("/nodes/{node_id}")
def read_node(node_id: int):
    if node_id >= len(AppConfig().nodes):
        raise HTTPException(status_code=404, detail="Node not found")

    node = AppConfig().nodes[node_id]

    return {
        "id": node.id,
        "ip": node.ip,
        "port": node.port,
        "ssh_user": node.ssh_user,
        "is_alive": node.is_alive()
    }


@app.get("/master")
def read_master_node():
    return AppConfig().master_node


def main(
        config_file: Annotated[Path, typer.Argument(
            help="The config file to read the cluster values from.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        )],
        host: Annotated[str, typer.Option(help='Host to bind to')] = '0.0.0.0',
        port: Annotated[int, typer.Option(help='Port to bind to')] = 8000
):
    AppConfig(config_file)
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    typer.run(main)
