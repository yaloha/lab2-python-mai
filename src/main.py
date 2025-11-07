import typer
import shlex

from src import log
from src.commands import cat, ls, cd, cp, mv, rm
from pathlib import Path

app = typer.Typer()

def register_commands(app: typer.Typer) -> None:
    """
    registration of created commands in typer app
    """
    cat.register_cat(app)
    ls.register_ls(app)
    cd.register_cd(app)
    cp.register_cp(app)
    mv.register_mv(app)
    rm.register_rm(app)

def main() -> None:
    """
    user inputs allowed pseudoshell commands until they enter 'quit'
    """
    register_commands(app)
    while True:
        inp = input(f"{Path.cwd()} $ ").strip()
        if inp == "quit":
            break
        try:
            comm = shlex.split(inp)
        except ValueError:
            typer.echo("Invalid command")
        if not comm:
            continue
        log.log_command(inp)
        try:
            result = app(comm, standalone_mode=False)
        except Exception as e:
            typer.echo(f"{e}")
            log.log_err("", e)

if __name__ == "__main__":
    main()
