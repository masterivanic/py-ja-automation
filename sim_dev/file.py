import json
import os
import shlex
import subprocess
from pathlib import Path
from pathlib import PosixPath
from pathlib import WindowsPath
from subprocess import CompletedProcess
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import List
from typing import Union

from sim_dev import GlobalVar


class Folder(object):
    """definition of a folder"""

    def __init__(self, folder_path: Path) -> None:
        if isinstance(folder_path, Path) and folder_path.exists():
            self._name: str = folder_path.name
            self._folder_path: Path = folder_path
        else:
            raise Exception("Folder doesn't exist")

    @property
    def name(self) -> str:
        return self._name

    @property
    def folder_path(self) -> Path:
        return self._folder_path

    def _is_folder(self) -> bool:
        """check if is folder or not"""
        return True if self.folder_path.is_dir() else False

    def get_sub_directory(self) -> List[Union[WindowsPath, PosixPath]]:
        if self._is_folder():
            list_folder: List[Union[WindowsPath, PosixPath]] = [
                folder for folder in self.folder_path.iterdir() if folder.is_dir()
            ]
            return list_folder

    def __repr__(self) -> str:
        return f"name:{self.name}"


class DirectoryTree:
    def __init__(self, root_path: Path, parent_path, is_last) -> None:
        self.root_path = root_path
        self.parent = parent_path
        self.is_last = is_last

    @property
    def displayname(self) -> str:
        if self.root_path.is_dir():
            return self.root_path.name
        return self.root_path.name

    @classmethod
    def _default_criteria(cls, path):
        return True

    @classmethod
    def make_tree(
        cls, root: Path, parent=None, is_last=False, criteria=None
    ) -> Generator["DirectoryTree", Any, Any]:
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(
            list(path for path in root.iterdir() if criteria(path)),
            key=lambda s: str(s).lower(),
        )

        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                folder = cls.make_tree(
                    path, parent=displayable_root, is_last=is_last, criteria=criteria
                )
                yield from folder
            else:
                yield cls(path, displayable_root, is_last)
            count += 1


class ReadCommandMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ReadCommandSingleton(metaclass=ReadCommandMeta):
    def __init__(self, path_default: str = "./sim_dev/commands/commands.json") -> None:
        with open(path_default, "r") as file:
            self.data: Dict = json.load(file)

    @property
    def get_data(self) -> Dict:
        return self.data

    def execute_cli_command(function: Callable) -> Callable[[str], Any]:
        def inner(command: str):
            args = shlex.split(command)
            processus: CompletedProcess[str] = subprocess.run(
                args, encoding="utf-8", text=True, stdout=subprocess.PIPE
            )
            try:
                if (_ := processus.returncode) == 0:
                    print("successfull execute!")
            except ChildProcessError as err:
                raise Exception(err.strerror)

        return inner

    @execute_cli_command
    def install_dependecies(self, command: str):
        ...

    @execute_cli_command
    def activate_python_project(self, command: str):
        ...

    @execute_cli_command
    def deactivate_python_project(self, command: str):
        ...

    @execute_cli_command
    def git_command(self, command: str):
        """use for check git installation"""
        ...


class FileManagement:
    """os service management"""

    def __init__(self, directory_name: str):
        self.paths = DirectoryTree.make_tree(
            root=Path(GlobalVar.get_right_path_from_platform()),
            criteria=self.is_not_hidden,
        )
        self._directory_name: Union[
            WindowsPath, PosixPath, None
        ] = self._search_project_directory(directory_name)
        self.command_executor = ReadCommandSingleton

    @property
    def get_directory_path(self) -> str:
        """to check, this raise NoneType Error and block app execution"""
        return self._directory_name.as_posix()

    def is_not_hidden(self, path):
        return not path.name.startswith(".")

    def _get_list_of_project(self, project_dir: str) -> List[str]:
        project_path = self._get_project_path(project_dir)
        if project_path:
            folders = [
                folder
                for folder in os.listdir(project_path)
                if os.path.isdir(project_path + "/" + folder)
            ]
            return folders
        return []

    def _check_poetry_installation(self) -> bool:
        try:
            is_poetry: bool = False
            list_env: List[str] = os.environ["PATH"].split(":")
            for item in list_env:
                if "poetry" in item or ".poetry" in item:
                    is_poetry = True
                    break
            return is_poetry
        except KeyError:
            raise Exception("System error!")

    def _check_git_installation(self) -> None:
        self.command_executor.git_command("git --version")

    def _search_project_directory(self, directory_name: str) -> Any:
        """
        :primary_path main path in a disk / on linux and X:/ on windows
        :directory_name: folder'name where is your python project
        :return the absolute path of your project i.e /home/any-path/your-project

        search your project in all folder in your system
        """
        file_full_path = None
        for file_path in self.paths:
            if file_path.displayname == directory_name:
                file_full_path = file_path.root_path.absolute()
                break
        return file_full_path

    def _check_docker_file(self) -> bool:
        file_list: List[str] = os.listdir(self.get_directory_path)
        if "Dockerfile" in file_list:
            return True
        return False

    def _open_and_launch_project(self):
        pass

    def _check_project_type(self) -> str:
        files = os.listdir(self._directory_name)
        if "pyproject.toml" in files:
            state = GlobalVar.POETRY_PROJECT.value
        elif "requirements.txt" in files:
            state = GlobalVar.PIP_PROJECT.value
        elif "mvnw" in files:
            state = GlobalVar.SPRING_PROJECT_MAVEN.value
        else:
            state = None
        return state

    def _activate_project_env(self) -> None:
        project = self._check_project_type()
        if project == "poetry":
            self.command_executor.activate_python_project(
                command=self.command_executor.get_data["python_command"]["poetry-shell"]
            )
        elif project == "pip":
            if value := input("Give path of your virtual env: "):
                command = value + "/" + "activate"
                path = Path(command)
                if path.exists():
                    self.command_executor.activate_python_project(command=command)
                else:
                    print("path given is incorrect or does not exist")

        elif project == "mvnw":
            # TO DO in maven case
            pass

    def _deactivate_project_env(self):
        project = self._check_project_type()
        if project == "poetry":
            self.command_executor.deactivate_python_project(
                command=self.command_executor.get_data["os_command"]["deactivate-env"]
            )
        elif project == "pip":
            if (value := input("Give path of your virtual env: ")) is not None:
                command = value + "/" + "deactivate"
                path = Path(command)
                if path.exists():
                    self.command_executor.activate_python_project(command=command)
                else:
                    print("path given is incorrect or does not exist")

    def _launch_docker_db(self):
        pass

    def _create_virtual_env(self):
        pass

    def _delete_virtual_env(self):
        # Optional feature:::
        pass

    def _install_project_dependencies(self):
        project = self._check_project_type()
        if project == "pip":
            self.command_executor.install_dependecies(
                self.command_executor.get_data["python_command"]["pip-install-req"]
            )
        elif project == "poetry":
            self.command_executor.install_dependecies(
                self.command_executor.get_data["python_command"]["poetry_install"]
            )


if __name__ == "__main__":
    folder = Folder(folder_path=Path(GlobalVar.LINUX_HOME_DIR.value))
    print(folder.get_sub_directory())
