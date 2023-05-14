import os
import shlex
import subprocess
from subprocess import CompletedProcess
from typing import List

from sim_dev import GlobalVar


class FileManagement:
    """os service management"""

    def _get_project_path(self, project_dir: str) -> str:
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
