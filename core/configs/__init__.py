import os

from dotenv import load_dotenv

from core.configs.consts import BASE_DIR

DOCKER_COMPOSE = os.getenv("DOCKER_COMPOSE", "false").lower() in ["true", "1", "yes"]
if not DOCKER_COMPOSE:
    env_path = BASE_DIR / "local.env"
    load_dotenv(verbose=True, dotenv_path=env_path)
