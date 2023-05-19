"""
 this is the entrypoint of our application
 define as module
"""
from sim_dev import __app_name__
from sim_dev import cli
from sim_dev.config import AppConfiguration
from sim_dev.file import FileManagement


def main() -> None:
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    # main()
    func = FileManagement()._search_project_directory(directory_name="simcore-packag")
    func()
