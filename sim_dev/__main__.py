"""
 this is the entrypoint of our application
 define as module
"""
from pathlib import Path

import typer

from sim_dev import __app_name__
from sim_dev import GlobalVar
from sim_dev.cli import CliCommand
from sim_dev.config import AppConfiguration
from sim_dev.file import DirectoryTree
from sim_dev.file import FileManagement
from sim_dev.file import Folder


def main():
    CliCommand()
    # print("Hello World")


if __name__ == "__main__":
    # main()
    # folder = Folder(folder_path=Path(GlobalVar.LINUX_HOME_DIR.value))
    # FileManagement().find_path("sim-dev")

    # With a criteria (skip hidden files)
    # def is_not_hidden(path):
    #     return not path.name.startswith(".")

    # paths = DirectoryTree.make_tree(Path("/home/simco-dev"), criteria=is_not_hidden)
    # for path in paths:
    #     if path.displayname == "sim_dev":
    #         print("dossier trouvé " + path.displayname)
    #         print(path.root_path.absolute())
    #         break
    #     else:
    #         print("ce n'est pas encore çà " + path.displayname)

    # directory = DirectoryTree(root_path=Path(GlobalVar.LINUX_HOME_DIR.value))
    # print(directory.format_tree())
    main()
    # file = FileManagement(directory_name="simenu")
    # file._check_git_installation()
