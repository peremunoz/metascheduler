from pathlib import Path
from fastapi import FastAPI
import typer
from typing_extensions import Annotated
from config.config import AppConfig


app = FastAPI()


@app.get("/")
@app.get("/status")
def read_status():
    return {"status": "ok"}


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
