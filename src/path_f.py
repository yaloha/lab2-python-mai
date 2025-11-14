import os
import typer

from src import log


def exp_path(path: str) -> str:
    """
    handling of ~ in path
    """
    if path.startswith("~"):
        path = os.path.expanduser(path)
    return path


def check_permission(path: str, command: str) -> bool:
    """
    check if file/directory can be accessed
    """
    if not os.access(path, os.R_OK):
        error = f"{command}: {path}: permission denied"
        typer.echo(error, err=True)
        log.log_err(command, error)
        return False
    return True


def check_dir_exists(path: str, command: str, lg: bool) -> bool:
    """
    check if directory exists
    """
    if not os.path.exists(path) or not os.path.isdir(path):
        if lg:
            error = f"{command}: {path}: no such directory"
            typer.echo(error, err=True)
            log.log_err(command, error)
        return False
    return True


def check_file_exists(path: str, command: str, lg: bool) -> bool:
    """
    check if file exists
    """
    if not os.path.exists(path) or os.path.isdir(path):
        if lg:
            error = f"{command}: {path}: no such file"
            typer.echo(error, err=True)
            log.log_err(command, error)
        return False
    return True
