import typer
from pathlib import Path
import os

def register_cat(app: typer.Typer) -> None:
    @app.command(help="print file contents")
    def cat(path: str = typer.Argument(help="file that you want to open")) -> None:
        try:
            file_path = Path(path)
            if not os.path.exists(file_path) or os.path.isdir(file_path):
                typer.echo(f"cat: {path}: no such file", err=True)
                return
            if not os.access(file_path, os.R_OK):
                typer.echo(f"cat: {path}: permission denied", err=True)
                return
            with open(file_path, 'r') as f:
                typer.echo(f.read())
        except Exception as e:
            typer.echo(f"cat: {path} gave an error: {e}", err=True)