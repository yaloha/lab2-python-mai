from datetime import datetime


def log_err(cm: str, err: str) -> None:
    """
    logging of errors
    """
    with open('shell.log', 'a') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ERROR: {err}\n')
        return

def log_success(cm:str) -> None:
    """
    logging of successful executions
    """
    with open('shell.log', 'a') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] command {cm} was successfully executed\n')
        return

def log_command(cm:str) -> None:
    """
    logging of starting command executions
    """
    with open('shell.log', 'a') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {cm}\n')
        return