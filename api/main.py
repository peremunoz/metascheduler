from contextlib import asynccontextmanager
import os
from pathlib import Path
import threading
from fastapi import FastAPI
import typer
import uvicorn
from typing_extensions import Annotated
from api.config.config import AppConfig
from api.routers import jobs, cluster, queues
from api.daemons.job_monitor import JobMonitorDaemon


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_background_daemon()
    yield
    stop_background_daemon()

app = FastAPI(lifespan=lifespan)

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
        ssh_key_file: Annotated[Path, typer.Option(
            help="The SSH key file to use to connect to the cluster nodes.",
            exists=False,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        )],
        ssh_user: Annotated[str, typer.Option(
            help="The SSH user to use to connect to the cluster nodes.",
        )] = 'metascheduler',
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
    if ssh_key_file:
        os.environ['SSH_KEY_FILE'] = str(ssh_key_file)
    os.environ['SSH_USER'] = ssh_user
    AppConfig(config_file, database_file)
    uvicorn.run(app, host=host, port=port)


def init_background_daemon():
    if os.getenv('TESTING') == 'true':
        return
    daemon = JobMonitorDaemon()
    daemon_thread = threading.Thread(target=daemon.start)
    daemon_thread.daemon = True
    daemon_thread.start()


def stop_background_daemon():
    if os.getenv('TESTING') == 'true':
        return
    daemon = JobMonitorDaemon()
    daemon.stop()


if __name__ == "__main__":
    typer.run(main)
