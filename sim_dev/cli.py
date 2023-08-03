from typing import List
from typing import Optional

import typer
from typer import Typer

from sim_dev import __app_name__
from sim_dev import __author__
from sim_dev import __version__
from sim_dev.config import AppConfiguration
from sim_dev.file import FileManagement

app: Typer = Typer(help="Awesome CLI python management app")
state = {"verbose": False}
file: FileManagement = FileManagement(directory_name="/home/simco-dev")


class CliCommand(Typer(help="Awesome CLI python management ap")):
    def __init__(self) -> None:
        self._app_configuration = AppConfiguration()

    def _app_version() -> None:
        typer.echo(f"{__app_name__} v{__version__} made by {__author__}")
        raise typer.Exit()

    def _app_directory_project(dir_project: str):
        file._check_git_installation()
        list_dir: List[str] = file._get_list_of_project(dir_project)
        count: int = 0
        if list_dir:
            for directory in list_dir:
                print(f"{count}:{directory}\n")
                count += 1
        else:
            typer.secho(f"{dir_project} don't exist", color=typer.colors.RED)
            raise typer.Exit(1)

    @app.command()
    def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application version",
            callback=_app_version,
            is_eager=True,
        )
    ) -> None:
        print("Will write verbose output")

    @app.command()
    def app_dir(
        version: Optional[str] = typer.Option(
            None,
            "--project-dir",
            help="List of all projetcs",
            callback=_app_directory_project,
            is_eager=True,
        )
    ) -> None:
        return
