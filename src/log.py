import os.path
from datetime import datetime


current_dir = os.path.abspath(__file__)
temp_dir = os.path.join(current_dir, "..", "temp")
log_file = os.path.join(temp_dir, "shell.log")

def ensure_log_dir() -> None:
    """Создает директорию для логов если её нет"""
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir, exist_ok=True)


def log_err(cm: str, err: str) -> None:
    """
    logging of errors
    """
    with open(log_file, 'a') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ERROR: {err}\n')
        return


def log_success(cm:str) -> None:
    """
    logging of successful executions
    """
    with open(log_file, 'a') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] command {cm} was successfully executed\n')
        return


def log_command(cm:str) -> None:
    """
    logging of starting command executions
    """
    with open(log_file, 'a') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {cm}\n')
        return