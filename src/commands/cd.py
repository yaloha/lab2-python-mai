import typer
import os

from src import path_f, log


def register_cd(app: typer.Typer) -> None:
    @app.command(help="change directory")
    def cd(
        path: str = typer.Argument(".", help="directory path")
    ) -> None:
        """
        cd - changes current working directory to the specified path
        """
        try:
            cm = "cd"
            path = path_f.exp_path(path)
            if not path_f.check_dir_exists(path, cm, 1):
                return
            os.chdir(path)
            log.log_success(cd)
        except Exception as e:
            log.log_err(cm, f"cd: {path}: {e}")
            typer.echo(f"cd: {path}: {e}", err=True)