import asyncio
from pathlib import Path

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from app import config

app_dir: Path = Path(__file__).parent.parent
locales_dir = app_dir / "locales"

event_loop = asyncio.get_event_loop()

storage = RedisStorage2(
    host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB
)

proxy_auth = aiohttp.BasicAuth(
    login=config.PROXY_USERNAME, password=config.PROXY_PASSWORD
)

bot = Bot(
    token=config.BOT_TOKEN,
    loop=event_loop,
    proxy=config.PROXY_URL,
    proxy_auth=proxy_auth,
)
dp = Dispatcher(bot, loop=event_loop, storage=storage,)


def setup():
    from app import middlewares
    from app.utils import executor

    middlewares.setup(dp)
    executor.setup()

    logger.info("Configure handlers...")
    # noinspection PyUnresolvedReferences
    import app.handlers
