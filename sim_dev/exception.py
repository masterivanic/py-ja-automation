from sim_dev import GlobalVar


class CommandFileError(Exception):
    """custom exception CommandFileError class"""

    def __init__(
        self, message=f"Command file not found at {GlobalVar.BASE_DIR.value} directory"
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CommandError(Exception):
    """custom exception CommandError class"""

    def __init__(self, message):
        self._message = message
        super().__init__(self._message)

    def __str__(self):
        return self._message
