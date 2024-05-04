from pathlib import Path
from fastapi import FastAPI
import typer
import uvicorn
from typing_extensions import Annotated
from api.config.config import AppConfig
from api.routers import jobs, cluster, queues


app = FastAPI()

app.include_router(jobs.router)
app.include_router(cluster.router)
app.include_router(queues.router)


@app.get("/")
@app.get("/status")
def read_status():
    return {"status": "running", "root": AppConfig().root}


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
        database_file: Annotated[Path, typer.Option(
            help="The database file to store the job queue.",
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=False,
            resolve_path=True,
        )] = None,
        host: Annotated[str, typer.Option(help='Host to bind to')] = '0.0.0.0',
        port: Annotated[int, typer.Option(help='Port to bind to')] = 8000
):
    AppConfig(config_file, database_file)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    typer.run(main)
