import os


class DotEnvNotProvidedError(ValueError):
    """env configuration is missing"""


def load_dotenv(f):
    """For debugging using PyCharm"""
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv(f), verbose=True)


for file in ["debug.env", ".env"]:
    load_dotenv(file)
    if os.getenv("DOTENV_LOADED", "False").lower() in ["true", "1", "yes"]:
        break
else:
    raise DotEnvNotProvidedError()
