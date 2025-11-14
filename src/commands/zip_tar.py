import shutil

import typer
import os

from src import path_f, log


def register_zip(app: typer.Typer) -> None:
    @app.command(help="converts directory to zip package")
    def zip(
        path_from: str = typer.Argument(".", help="path which we're zipping directory"),
        zip_name: str = typer.Argument(".", help="name of the zip we're creating"),
    ) -> None:
        """
        zip - zips path_from to zip package with name zip_name
        """
        try:
            cm = "zip"
            path_from = path_f.exp_path(path_from)
            zip_name = path_f.exp_path(zip_name)
            if not path_f.check_dir_exists(path_from, cm, 1):
                return
            if not path_f.check_permission(path_from, cm):
                return
            shutil.make_archive(zip_name,'zip', path_from)
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, f"zip: {path_from}, {zip_name}: {e}")
            typer.echo(f"zip: {path_from}, {zip_name}: {e}", err=True)


def register_unzip(app: typer.Typer) -> None:
    @app.command(help="extracts zip archives")
    def unzip(
            path_from: str = typer.Argument(..., help="path to the zip file")
    ) -> None:
        """
        unzip - extracts zip archives to specified directory
        """
        try:
            cm = "unzip"
            path_from = path_f.exp_path(path_from)
            if not path_f.check_file_exists(path_from, cm, 1):
                return
            if not path_f.check_permission(path_from, cm):
                return
            shutil.unpack_archive(path_from, '.', 'zip')
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, f"unzip: {path_from}: {e}")
            typer.echo(f"unzip: {path_from}: {e}", err=True)


def register_tar(app: typer.Typer) -> None:
    @app.command(help="converts directory to zip package")
    def tar(
        path_from: str = typer.Argument(".", help="path of the directory which we're making a tar archive"),
        zip_name: str = typer.Argument(".", help="name of the tar archive we're creating"),
    ) -> None:
        """
        tar - makes tar archive from path_from with name zip_name
        """
        try:
            cm = "tar"
            path_from = path_f.exp_path(path_from)
            zip_name = path_f.exp_path(zip_name)
            if not path_f.check_dir_exists(path_from, cm, 1):
                return
            if not path_f.check_permission(path_from, cm):
                return
            shutil.make_archive(zip_name, 'tar', path_from)
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, f"zip: {path_from}, {zip_name}: {e}")
            typer.echo(f"zip: {path_from}, {zip_name}: {e}", err=True)


def register_untar(app: typer.Typer) -> None:
    @app.command(help="extracts zip archives")
    def untar(
            path_from: str = typer.Argument(..., help="path to the tar file")
    ) -> None:
        """
        unzip - extracts tar archives to specified directory
        """
        try:
            cm = "untar"
            path_from = path_f.exp_path(path_from)
            if not path_f.check_file_exists(path_from, cm, 1):
                return
            if not path_f.check_permission(path_from, cm):
                return
            shutil.unpack_archive(path_from, '.', 'tar')
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, f"untar: {path_from}: {e}")
            typer.echo(f"untar: {path_from}: {e}", err=True)