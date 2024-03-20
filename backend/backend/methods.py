import os
from dotenv import load_dotenv

load_dotenv()


def get_bool_env(env_var, default=True):
    value = os.getenv(env_var)
    if value is None:
        return default
    return value.lower() in ('true', '1')
