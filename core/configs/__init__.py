import os


class EnvNotImplementedError(NotImplementedError):
    """env configuration is missing"""


def load_debug_dotenv():
    """For debugging using PyCharm"""
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv("debug.env"), verbose=True)


env = os.getenv("BOT_TOKEN") is not None
if not env:
    load_debug_dotenv()
    env = os.getenv("BOT_TOKEN") is not None
    if not env:
        raise EnvNotImplementedError()
