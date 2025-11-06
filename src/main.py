import typer
import shlex
from src.commands import cat, ls, cd
from pathlib import Path

app = typer.Typer()

@app.command()
def shell() -> None:
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
        #log
        result = app(comm, standalone_mode=False)


def register_commands(app: typer.Typer) -> None:
    cat.register_cat(app)
    ls.register_ls(app)
    cd.register_cd(app)

def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    app()

if __name__ == "__main__":
    main()
