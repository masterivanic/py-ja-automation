import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional

from sim_dev import GlobalVar
from sim_dev.exception import CommandFileError


class AppConfigurationInstance(object):
    def __new__(cls) -> Any:
        if not hasattr(cls, "instance"):
            cls.instance = super(AppConfigurationInstance, cls).__new__(cls)
        return cls.instance


class AppConfiguration(AppConfigurationInstance):
    """access command file"""

    def _check_command_file_exists(self) -> bool:
        files: List[str] = os.listdir(
            os.path.join(GlobalVar.BASE_DIR.value, "commands")
        )
        if files and files[0].endswith(".json"):
            return True
        return False

    def _get_args_command(self, command_key: Optional[str] = None) -> str:
        is_conf_file = self._check_command_file_exists()
        if not is_conf_file:
            raise CommandFileError
        else:
            file_config_path: str = os.path.join(
                GlobalVar.BASE_DIR.value, "commands/commands.json"
            )
            with open(file_config_path, "r") as file:
                data = json.load(file)
                tab_dicts: List[dict] = [value for key, value in data.items()]
                flat_dict: ChainMap = ChainMap(*tab_dicts)  # flat all dict in one dict
                command = flat_dict.get(command_key)
            return command

    def _get_static_logo(self) -> str:
        file_config_path: str = os.path.join(
            GlobalVar.BASE_DIR.value, "static/logo.txt"
        )
        with open(file_config_path, "r") as file:
            data: str = file.read()
        return data


if __name__ == "__main__":
    pass
