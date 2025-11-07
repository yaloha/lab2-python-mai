import typer
from pathlib import Path
import os

from src import path_f, log


def register_cat(app: typer.Typer) -> None:
    @app.command(help="print file contents")
    def cat(path: str = typer.Argument(help="file that you want to open")) -> None:
        """
        cat - output contents of specified file that resides at path you specify
        """
        try:
            cm = "cat"
            path = path_f.exp_path(path)
            if not path_f.check_file_exists(path, cm, 1):
                return
            if not path_f.check_permission(path, cm):
                return
            with open(path, 'r') as f:
                typer.echo(f.read())
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, f"cat: {path} gave an error: {e}")
            typer.echo(f"cat: {path} gave an error: {e}", err=True)