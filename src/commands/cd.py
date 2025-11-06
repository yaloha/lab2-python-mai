import typer
import os


def register_cd(app: typer.Typer) -> None:
    @app.command(help="change directory")
    def cd(
        path: str = typer.Argument(".", help="directory path")
    ) -> None:
        try:
            if path.startswith("~"):
                path = os.path.expanduser(path)

            if not os.path.exists(path) or not os.path.isdir(path):
                typer.echo(f"cd: {path}: no such directory", err=True)
                return

            os.chdir(path)
        except Exception as e:
            typer.echo(f"cd: {path}: {e}", err=True)