import shutil

import typer
import os

from src import path_f, log


def register_mv(app: typer.Typer) -> None:
    @app.command(help="moves file/directory or renames file/directory")
    def mv(
        path_from: str = typer.Argument(".", help="path which we're moving/renaming"),
        path_to: str = typer.Argument(".", help="path which we're moving to"),
    ) -> None:
        """
        mv - moves path_from to path_to or renames path_from to path_to
        """
        try:
            cm = "mv"
            path_from = path_f.exp_path(path_from)
            path_to = path_f.exp_path(path_to)
            print(path_from, path_to)
            if not os.path.exists(path_from):
                typer.echo(f"mv: {path_from}: no such file or directory", err=True)
                return
            path_f.check_permission(path_from, cm)
            if path_f.check_dir_exists(path_to, cm, 0):
                if not path_f.check_permission(path_to, cm):
                    return
                path_to = os.path.join(path_to, os.path.basename(path_from))
            shutil.move(path_from, path_to)
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, f"mv: {path_from}, {path_to}: {e}")
            typer.echo(f"mv: {path_from}, {path_to}: {e}", err=True)