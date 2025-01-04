import os
from functools import wraps

LOG_FILE = rf"{os.getcwd()}\log.txt"


def log_to_file(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as f:
                f.write("")
        with open(LOG_FILE, "a") as f:
            try:
                result = func(self, *args, **kwargs)
                if result is not None:
                    f.write(f"{result} \n")
                return result
            except Exception as e:
                f.write(f"Error in {func.__name__}: {e}\n")
                raise

    return wrapper
