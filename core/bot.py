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

from core.configs import consts, proxy, redis, telegram, webhook
from core.configs.consts import LOGS_FOLDER
from core.database import db_worker
from core.utils.middlewares.logging_middleware import LoguruLoggingMiddleware
from core.utils.middlewares.update_middleware import UpdateUserMiddleware

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s : %(name)s : %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d at %H:%M:%S",
)

logger.remove()

logger.add(
    LOGS_FOLDER / "debug_logs.log",
    format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
    level=logging.DEBUG,
)

logger.add(
    LOGS_FOLDER / "info_logs.log",
    format="[{time:YYYY-MM-DD at HH:mm:ss}] {level}: {name} : {message}",
    level=logging.INFO,
)

logger.add(
    LOGS_FOLDER / "warn_logs.log",
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
if proxy.PROXY_USE:
    proxy_url = proxy.PROXY_URL
    if len(proxy.PROXY_USERNAME) > 0:
        proxy_auth = aiohttp.BasicAuth(
            login=proxy.PROXY_USERNAME, password=proxy.PROXY_PASSWORD
        )
event_loop = asyncio.get_event_loop()
bot = Bot(
    token=telegram.BOT_TOKEN, loop=event_loop, proxy=proxy_url, proxy_auth=proxy_auth,
)
dp = Dispatcher(
    bot,
    loop=event_loop,
    storage=RedisStorage2(
        redis.REDIS_HOST,
        redis.REDIS_PORT,
        db=redis.REDIS_DB,
        prefix=redis.REDIS_PREFIX,
    ),
)


async def on_startup(dispatcher: aiogram.Dispatcher):
    if webhook.WEBHOOK_USE:
        await dispatcher.bot.set_webhook(webhook.WEBHOOK_LISTEN)

    me = await dispatcher.bot.get_me()

    logger.warning(f'Powering up @{me["username"]}')
    logger.warning(f"BASE_DIR {consts.BASE_DIR}")
    dp.middleware.setup(LoguruLoggingMiddleware())
    dp.middleware.setup(UpdateUserMiddleware())

    from core.handlers import register_handlers

    register_handlers()

    signal.signal(signal.SIGTERM, terminate)


async def on_shutdown(dispatcher: aiogram.Dispatcher):
    logger.warning("Shutting down..")

    # Close storage
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    # close db session
    db_worker.on_shutdown(dp)

    if webhook.WEBHOOK_USE:
        await dispatcher.bot.delete_webhook()

    logger.warning("Bye!")


def terminate(signalnum, frame):
    logger.warning(f"!! received {signalnum}, terminating the process")
    sys.exit()


def run():
    if webhook.WEBHOOK_USE:
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=webhook.WEBHOOK_LISTEN,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=False,
            host=webhook.WEBHOOK_HOST,
            port=webhook.WEBHOOK_PORT,
        )
    else:
        executor.start_polling(
            dp, on_startup=on_startup, on_shutdown=on_shutdown, timeout=20,
        )
