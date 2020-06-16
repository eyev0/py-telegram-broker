import os

from dotenv import find_dotenv, load_dotenv

DOCKER_COMPOSE = os.getenv("DOCKER_COMPOSE", "false").lower() in ["true", "1", "yes"]
if not DOCKER_COMPOSE:
    load_dotenv(find_dotenv(), verbose=True)
