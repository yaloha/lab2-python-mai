import typer
import os
import re

from src import path_f, log


def register_grep(app: typer.Typer) -> None:
    @app.command(help="search for a given pattern")
    def grep(
            pattern: str = typer.Argument(help="pattern to search for"),
            given_path: str = typer.Argument(help="file or directory in which we're searching"),
            case: bool = typer.Option(False, "-i", help="ignore case"),
            rec: bool = typer.Option(False, "-r", help="search recursively in subdirectories")
    ) -> None:
        """
        grep - search for a given pattern
        """
        try:
            cm = "grep"
            given_path = path_f.exp_path(given_path)
            if not os.path.exists(given_path):
                typer.echo(f"grep: {given_path}: no such path", err=True)
                log.log_err(cm, f"grep: {given_path}: no such path")
                return
            if not path_f.check_permission(given_path, cm):
                return
            regex = re.compile(pattern, re.IGNORECASE if case else 0)

            def file_search(path, lg):
                try:
                    lines = []
                    with open(path, 'r') as file:
                        for line_num, line in enumerate(file, 1):
                            if regex.search(line):
                                line = line.strip()
                                lines.append(f"{path}: {line_num}: {line}".strip())
                    return lines
                except Exception:
                    pass
                if lg:
                    typer.echo(f"grep: {path}: nothing found", err=True)
                    log.log_err(cm, f"grep: {path}: nothing found")
                return

            def rec_search(path, lg):
                res_list = []
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        res = file_search(file_path, 0)
                        if res:
                            res_list.append(res)
                    if not dirs:
                        return res_list
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        res = rec_search(dir_path, 0)
                        if res:
                            for line in res:
                                res_list.append(line)
                    if res_list:
                        return res_list
                if lg:
                    typer.echo(f"grep: {path}: nothing found", err=True)
                    log.log_err(cm, f"grep: {path}: nothing found")
                return
            if path_f.check_file_exists(given_path, cm, 0):
                res = file_search(given_path, 1)
                if not res:
                    return
                for line in res:
                    typer.echo(line)
            elif path_f.check_dir_exists(given_path, cm, 0):
                if rec:
                    res = rec_search(given_path, 1)
                    if not res:
                        return
                    for lines in res:
                        for line in lines:
                            typer.echo(line)
                else:
                    typer.echo(f"grep: {given_path}: is a directory, flag -r is required", err=True)
                    log.log_err(cm, f"grep: {given_path}: is a directory, flag -r is required")
                    return
            log.log_success(cm)
        except Exception as e:
            log.log_err(cm, f"grep: {pattern}, {given_path}: {e}")
            typer.echo(f"grep: {pattern}, {given_path}: {e}", err=True)
