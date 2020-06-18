import secrets

from envparse import env


class DotEnvNotProvidedError(ValueError):
    """env configuration is missing"""


def load_dotenv(f):
    """For debugging using PyCharm"""
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv(f), verbose=True)


for file in ["debug.env", ".env"]:
    load_dotenv(file)
    if env.bool("DOTENV_LOADED", default=False):
        break
else:
    raise DotEnvNotProvidedError()


BOT_TOKEN = env.str("BOT_TOKEN", default="")
BOT_SU = env.str("BOT_SU", default="").split(",")
BOT_ADMINS = []

POSTGRES_USER = env.str("POSTGRES_USER", default="docker")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="")
POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_DB = env.str("POSTGRES_DB", default="docker")
POSTGRES_URI = (
    f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

REDIS_HOST = env.str("REDIS_HOST", default="redis")
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_DB = env.int("REDIS_DB", default=0)

PROXY_USE = env.bool("PROXY_USE", default=False)
PROXY_URL = env.str("PROXY_URL", default="")
PROXY_USERNAME = env.str("PROXY_USERNAME", default="")
PROXY_PASSWORD = env.str("PROXY_PASSWORD", default="")

DOMAIN = env.str("DOMAIN", default="example.com")
SECRET_KEY = secrets.token_urlsafe(48)
WEBHOOK_BASE_PATH = env.str("WEBHOOK_BASE_PATH", default="/webhook")
WEBHOOK_PATH = f"{WEBHOOK_BASE_PATH}/{SECRET_KEY}"
WEBHOOK_URL = f"https://{DOMAIN}{WEBHOOK_PATH}"
BOT_PUBLIC_PORT = env.int("BOT_PUBLIC_PORT", default=8080)
