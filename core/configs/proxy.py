import os

PROXY_USE = bool(os.getenv("PROXY_USE", "False"))
PROXY_URL = os.getenv("PROXY_URL", "socks5://0.0.0.0:1080")
PROXY_USERNAME = os.getenv("PROXY_USERNAME", "")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD", "")
