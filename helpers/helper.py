from datetime import datetime


def print_log_error(func_name, error, now=datetime.now()):
    print(f">>> ERROR [{now}][{func_name}] >> {error}")