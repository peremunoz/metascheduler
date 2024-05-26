import typer
import os

app = typer.Typer(no_args_is_help=True)


@app.command()
def cluster_mode():
    print(
        f"Getting cluster mode from {os.getenv('API_IP')}:{os.getenv('API_PORT')}")


if __name__ == "__main__":
    app()
