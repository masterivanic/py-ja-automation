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
    main()
    # conf = AppConfiguration()
    # val = conf._check_command_file_exists()
    # print(val)
