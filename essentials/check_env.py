import os
import functools

REQUIRED_ENV_VARS = ['DB_URL', 'DB_KEY']

def check_env(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing:
            raise EnvironmentError(
                f'Missing environment variables: {', '.join(missing)}'
            )
        return func(*args, **kwargs)
    return wrapper
