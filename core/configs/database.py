import os

DB_HOST_URL = os.getenv("DB_HOST_URL", "postgres://docker:docker@db:5432/docker")
