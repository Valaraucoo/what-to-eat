from typer.testing import CliRunner

from wte.main import app

runner = CliRunner()


def test_ls_without_config() -> None:
    result = runner.invoke(app, ["ls", "--profile", "invalid"])
    assert result.exit_code == 1
    assert result.output == "💥 Config file not found, run what-to-eat configure first\n"
