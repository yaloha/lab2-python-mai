from datetime import datetime

import typer
from stat import filemode
import os

def register_ls(app: typer.Typer) -> None:
    @app.command(help="print all files in directory")
    def ls(
        path: str = typer.Argument(".", help="directory path"),
        details: bool = typer.Option(False, "-l", help="file info")
    ) -> None:
        try:
            if path.startswith("~"):
                path = os.path.expanduser(path)
            if not os.path.exists(path) or not os.path.isdir(path):
                typer.echo(f"ls: {path}: no such directory", err=True)
                return
            if not os.access(path, os.R_OK):
                typer.echo(f"ls: {path}: permission denied", err=True)
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
        except Exception as e:
            typer.echo(f"ls: {path} gave an error: {e}", err=True)