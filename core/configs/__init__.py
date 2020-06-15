from dotenv import load_dotenv

from core.configs.consts import BASE_DIR

env_path = BASE_DIR / "local.env"
load_dotenv(verbose=True, dotenv_path=env_path)
