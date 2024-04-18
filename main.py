from typing import Optional
from pathlib import Path
import typer
from typing_extensions import Annotated
from interfaces.Cluster import Cluster

def main(
        config: Annotated[Optional[Path], typer.Option(
            help="The config file to read the cluster values from.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            )] = None
        ):
    """
    Main function of the program.

    """
    cluster: Cluster = Cluster()
    if config is not None:
        print(f"Reading the cluster config from {config}")
        cluster.setup_from_file(config)
    else:
        cluster.manual_setup()

    

if __name__ == '__main__':
    typer.run(main)