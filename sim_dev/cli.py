from typing import List
from typing import Optional

import typer
from typer import Typer

from sim_dev import __app_name__
from sim_dev import __author__
from sim_dev import __version__
from sim_dev.config import AppConfiguration
from sim_dev.file import FileManagement

app: Typer = Typer()
file: FileManagement = FileManagement()


class CliCommand:
    def __init__(self, app_configuration: AppConfiguration = AppConfiguration) -> None:
        self._app_configuration = app_configuration

    def _app_version(value: bool) -> None:
        if value:
            typer.echo(f"{__app_name__} v{__version__} made by {__author__}")
            raise typer.Exit()

    def _app_directory_project(dir_project: str):
        file.check_git_installation()
        list_dir: List[str] = file._get_list_of_project(dir_project)
        count: int = 0
        if list_dir:
            for directory in list_dir:
                print(f"{count}:{directory}\n")
                count += 1
        else:
            typer.secho(f"{dir_project} don't exist", color=typer.colors.RED)
            raise typer.Exit(1)

    @app.callback()
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
        return

    @app.callback()
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
