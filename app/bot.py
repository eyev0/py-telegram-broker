import asyncio
import logging
import signal
import sys

import aiogram
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils import executor
from loguru import logger

from app import config
from app.database import db_worker
from app.utils.middlewares.logging_middleware import LoguruLoggingMiddleware
from app.utils.middlewares.update_middleware import UpdateUserMiddleware

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s : %(name)s : %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d at %H:%M:%S",
)

logger.remove()

logger.add(
    config.LOGS_FOLDER / "debug_logs.log",
    format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
    level=logging.DEBUG,
)

logger.add(
    config.LOGS_FOLDER / "info_logs.log",
    format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
    level=logging.INFO,
)

logger.add(
    config.LOGS_FOLDER / "warn_logs.log",
    format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
    level=logging.WARNING,
)

logger.add(
    sys.stderr,
    format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
    level=logging.INFO,
    colorize=False,
)

logging.getLogger("aiogram").setLevel(logging.INFO)

proxy_url = None
proxy_auth = None
if config.PROXY_USE:
    proxy_url = config.PROXY_URL
    if len(config.PROXY_USERNAME) > 0:
        proxy_auth = aiohttp.BasicAuth(
            login=config.PROXY_USERNAME, password=config.PROXY_PASSWORD
        )
event_loop = asyncio.get_event_loop()
bot = Bot(
    token=config.BOT_TOKEN, loop=event_loop, proxy=proxy_url, proxy_auth=proxy_auth,
)
dp = Dispatcher(
    bot,
    loop=event_loop,
    storage=RedisStorage2(
        config.REDIS_HOST,
        config.REDIS_PORT,
        db=config.REDIS_DB,
        prefix=config.REDIS_PREFIX,
    ),
)


async def on_startup(dispatcher: aiogram.Dispatcher):
    if config.WEBHOOK_USE:
        await dispatcher.bot.set_webhook(config.WEBHOOK_LISTEN)

    me = await dispatcher.bot.get_me()

    logger.warning(f'Powering up @{me["username"]}')
    logger.warning(f"BASE_DIR {config.BASE_DIR}")
    dp.middleware.setup(LoguruLoggingMiddleware())
    dp.middleware.setup(UpdateUserMiddleware())

    from app.handlers import register_handlers

    register_handlers()

    signal.signal(signal.SIGTERM, terminate)


async def on_shutdown(dispatcher: aiogram.Dispatcher):
    logger.warning("Shutting down..")

    # Close storage
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    # close db session
    db_worker.on_shutdown(dp)

    if config.WEBHOOK_USE:
        await dispatcher.bot.delete_webhook()

    logger.warning("Bye!")


def terminate(signalnum, frame):
    logger.warning(f"!! received {signalnum}, terminating the process")
    sys.exit()


def run():
    if config.WEBHOOK_USE:
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_LISTEN,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=False,
            host=config.WEBHOOK_HOST,
            port=config.WEBHOOK_PORT,
        )
    else:
        executor.start_polling(
            dp, on_startup=on_startup, on_shutdown=on_shutdown, timeout=20,
        )
