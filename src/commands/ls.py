from datetime import datetime

import typer
from stat import filemode
import os

from src import path_f, log


def register_ls(app: typer.Typer) -> None:
    @app.command(help="print all files in directory")
    def ls(
        path: str = typer.Argument(".", help="directory path"),
        details: bool = typer.Option(False, "-l", help="file info")
    ) -> None:
        try:
            cm = "ls"
            path = path_f.exp_path(path)
            if not path_f.check_dir_exists(path, cm, 1):
                return
            if not path_f.check_permission(path, cm):
                return
            files = os.listdir(path)
            if details:
                for file in files:
                    file_path = os.path.join(path, file)
                    file_size = os.stat(file_path).st_size
                    permissions = filemode(os.stat(file_path).st_mode)
                    time = datetime.fromtimestamp(os.stat(file_path).st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    typer.echo(f"{permissions} {file_size:8} {time} {file}")
            else:
                for file in files:
                    typer.echo(file)
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, f"ls: {path} gave an error: {e}")
            typer.echo(f"ls: {path} gave an error: {e}", err=True)