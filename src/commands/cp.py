import shutil

import typer
import os

from src import path_f, log


def register_cp(app: typer.Typer) -> None:
    @app.command(help="copy file/directory")
    def cp(
        path_from: str = typer.Argument(".", help="path which we're copying from"),
        path_to: str = typer.Argument(".", help="path which we're copying to"),
        rec: bool = typer.Option(False, "-r", help="specifies if copying is recursive")
    ) -> None:
        """
        cp - copies file/directory (only if you use flag -r) from path_from to path_to"
        """
        try:
            cm = "cp"
            path_from = path_f.exp_path(path_from)
            path_to = path_f.exp_path(path_to)
            if rec:
                if path_f.check_dir_exists(path_to, cm, 0):
                    path_to = os.path.join(path_to, path_from)
                    shutil.copytree(path_from, path_to)
                    log.log_success(cm)
                    return
                else:
                    shutil.copytree(path_from, path_to)
                    log.log_success(cm)
                    return
            else:
                if path_f.check_dir_exists(path_from, cm, 0):
                    typer.echo("cp: use -r flag to copy a directory", err=True)
                    log.log_err(cm, "cp: use -r flag to copy a directory")
                    return
                else:
                    if path_f.check_file_exists(path_from, cm, 1) and path_f.check_dir_exists(path_to, cm, 1):
                        shutil.copy2(path_from, path_to)
                        log.log_success(cm)
                        return
        except Exception as e:
            log.log_err(cm, f"cd: {path_from}, {path_to}: {e}")
            typer.echo(f"cd: {path_from}, {path_to}: {e}", err=True)