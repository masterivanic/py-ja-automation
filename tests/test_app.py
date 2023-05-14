from typer.testing import CliRunner

from sim_dev import __app_name__
from sim_dev import __author__
from sim_dev import __version__
from sim_dev import cli
from sim_dev.config import AppConfiguration

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__} made by {__author__}\n" in result.stdout


def test_commands_args():
    conf = AppConfiguration()
    config = AppConfiguration()
    result = conf._get_args_command("change-directory")
    result1 = config._get_args_command("")
    result2 = config._get_args_command(None)

    assert not result is None
    assert conf is config
    assert not result == result1
    assert result2 is None
