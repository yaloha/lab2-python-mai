import shutil

import typer
import os

from src import path_f, log


def register_rm(app: typer.Typer) -> None:
    @app.command(help="remove file/directory")
    def rm(
        path: str = typer.Argument(".", help="path of file/directory which we are deleting"),
        rec: bool = typer.Option(False, "-r", help="specifies whether deleting is recursive"),
    ) -> None:
        """
        rm - removes specified file/directory (only if you use flag -r), asks for confirmation before doing so
        """
        try:
            cm = "rm"
            path = path_f.exp_path(path)
            if not os.path.exists(path):
                log.log_err(cm, "no such file/directory")
                typer.echo("rm: no such file/directory")
                return
            if not path_f.check_permission(path, cm):
                return
            if path in ['/', '..']:
                typer.echo("can't delete this directory", err=True)
                log.log_err(cm, "can't delete this directory")
                return
            agr = input("are you sure? Y/n\n")
            if agr:
                if path_f.check_dir_exists(path, cm, 0):
                    if rec:
                        shutil.rmtree(path)
                    else:
                        typer.echo(typer.echo("rm: use -r flag to delete a directory", err=True))
                        log.log_err(cm, "rm: use -r flag to delete a directory")
                        return
                else:
                    if os.path.exists(path):
                        os.remove(path)
                    else:
                        typer.echo("rm: no such file or directory", err=True)
                        log.log_err(cm, "rm: no such file or directory")
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, "rm: {path}: {e}")
            typer.echo(f"rm: {path}: {e}", err=True)