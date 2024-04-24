from fastapi import FastAPI
import typer
from typing_extensions import Annotated


app = FastAPI()


@app.get("/")
@app.get("/status")
def read_status():
    return {"status": "ok"}


def main(host: Annotated[str, typer.Option(help='Host to bind to')] = '0.0.0.0',
         port: Annotated[int, typer.Option(help='Port to bind to')] = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    typer.run(main)
