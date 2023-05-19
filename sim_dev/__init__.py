import os
from enum import Enum
from pathlib import Path
from sys import platform
from typing import Final

__app_name__ = "sim_dev"
__version__ = "0.0.1"
__author__ = "SIMCO"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    ID_ERROR,
) = range(4)


ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
}


class GlobalVar(Enum):
    """
    do to assign value cause and enum could not reattribute a data unless
    of herit of EnumMeta and override
    """

    BASE_DIR: Final[Path] = Path(__file__).resolve().parent.absolute()
    POETRY_PROJECT: Final[str] = "poetry"
    PIP_PROJECT: Final[str] = "pip"
    HOME_DIR: str
    LINUX_HOME_DIR: Final[str] = os.path.abspath(os.environ["HOME"])
    INTERACTIVE_MODE: Final[int] = 0

    @classmethod
    def get_right_path_from_platform(cls) -> str:
        if platform == "linux":
            cls.HOME_DIR = os.path.abspath(os.environ["HOME"])
        elif platform == "win32":
            cls.HOME_DIR = os.path.abspath(os.sep)
        return cls.HOME_DIR
