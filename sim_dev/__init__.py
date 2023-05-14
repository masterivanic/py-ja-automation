""" This module does stuff."""
import os
from enum import Enum
from pathlib import Path
from typing import Final

__app_name__ = "sim-dev"
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
    BASE_DIR: Final[Path] = Path(__file__).resolve().parent.absolute()
    POETRY_PROJECT: Final[str] = "poetry"
    PIP_PROJECT: Final[str] = "pip"
    LINUX_HOME_DIR: Final[str] = os.path.abspath(os.environ["HOME"])
    INTERACTIVE_MODE: Final[int] = 0
