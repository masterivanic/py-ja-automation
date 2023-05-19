import os
import shlex
import subprocess
from pathlib import Path
from pathlib import PosixPath
from pathlib import WindowsPath
from subprocess import CompletedProcess
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from sim_dev import GlobalVar


class Folder(object):
    """definition of a folder"""

    def __init__(self, name: str, folder_path: Path) -> None:
        self._name = name
        self._folder_path = folder_path

    @property
    def folder_path(self) -> Path:
        return self._folder_path

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    def __new__(cls, *args: Any, **kwds: Any) -> Any:
        if isinstance(cls.folder_path, Path) and cls.folder_path.exists():
            return super(Folder, cls).__new__(cls, *args, **kwds)
        else:
            raise Exception("Folder doesn't exist")

    def is_folder(self) -> bool:
        return True if self.folder_path.is_dir() else False

    def get_sub_directory(self) -> List[Union[WindowsPath, PosixPath]]:
        if self.is_folder():
            list_folder: List[Union[WindowsPath, PosixPath]] = [
                x for x in self.folder_path.iterdir() if x.is_dir()
            ]
            return list_folder


class DirectoryTree:
    directory: Dict[str, List[Folder]] = {"root": None, "children": None}

    def __init__(self, root: Optional[str], children: List[Folder]) -> None:
        self._root = root
        self._children = children

    @property
    def root(self) -> str:
        return self._root

    @property
    def children(self) -> List[Folder]:
        return self._children

    def to_tree(self) -> Dict[str, Folder]:
        path_folder = os.path.abspath(self.root)
        folder: Folder = Folder(name=self.root, folder_path=path_folder)

        list_sub = [
            Folder(name=p.name, folder_path=p.resolve())
            for p in folder.get_sub_directory()
        ]
        self.directory["root"] = folder.name
        self.directory["children"] = list_sub

        return self.directory

    def __new__(cls) -> Any:
        return cls(*cls.to_tree)


class FileManagement:
    """os service management"""

    def _get_project_path(self, project_dir: str) -> str:
        """to check, this raise NoneType Error and block app execution"""
        project_path = os.path.abspath(
            GlobalVar.LINUX_HOME_DIR.value + "/" + project_dir
        )
        if os.path.isdir(project_path):
            return project_path
        return None

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

    def _check_git_installation(self) -> bool:
        cmd_line = "git --version"
        args = shlex.split(cmd_line)
        processus: CompletedProcess[str] = subprocess.run(
            args, encoding="utf-8", text=True, stdout=subprocess.PIPE
        )
        return True if processus.returncode == 0 else False

    def find_path(self, directory_name: str) -> str:
        """surcharge des methodes
        use linux cmd instead:  find . -type d -iname "directoryName" -print
        """
        pass

    def find_path(self, primary_path: str, directory_name: str) -> str:
        """
        :primary_pathm main path in a disk / on linux and X:/ on windows
        :directory_name: folder'name here is your python project
        :return the absolute path of your project i.e /home/any-path/your-project

        search your project in all folder in your system
        """
        # import pdb; pdb.set_trace()
        print(primary_path)
        if os.path.isdir(primary_path):
            list_dir = os.listdir(primary_path)
            if directory_name in list_dir:
                print("dossier trouvé")
                print(primary_path)
                exit(1)
            else:
                for folder in os.listdir(primary_path):
                    if "." not in folder:
                        primary_path += "/"
                        primary_path += folder
                        path_as_string = os.path.abspath(primary_path)

                        print(path_as_string, "-----------> path of folder")
                        if os.path.isdir(path_as_string):
                            self.find_path(path_as_string, directory_name)
                        # else:
                        #     time.sleep(3)
                        #     print(f"{folder} is not a folder")
                        #     continue
                    else:
                        print(f"non trouvé")
        return primary_path

    def _search_project_directory(
        self,
        directory_name: str = None,
    ):
        primary_path: str = GlobalVar.get_right_path_from_platform()
        self.find_path(primary_path, directory_name)

    def _check_docker_file(self) -> bool:
        pass

    def _open_and_launch_project(self):
        pass

    def _check_project_type(self, project_dir: str) -> str:
        files = os.listdir(project_dir)
        if "pyproject.toml" in files:
            state = GlobalVar.POETRY_PROJECT.value
        elif "requirements.txt" in files:
            state = GlobalVar.PIP_PROJECT.value
        else:
            state = None
        raise state

    def _activate_project_env(self):
        pass

    def _deactivate_project_env(self):
        pass

    def _launch_docker_db(self):
        pass

    def _create_virtual_env(self):
        pass

    def _delete_virtual_env(self):
        # Optional feature:::
        pass

    def _install_project_dependencies(self):
        pass
