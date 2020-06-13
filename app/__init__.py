import asyncio
import logging
import os
import signal
import sys
from datetime import datetime

import aiogram
import aiohttp
import pytz
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from app.config import Config, ConfigManager

clock = datetime(2020, 1, 1, tzinfo=pytz.timezone('Europe/Moscow'))

debug = bool(os.getenv('PY_APP_DEBUG_MODE', 'False'))
config = ConfigManager(debug).config

stdout_handler = logging.StreamHandler(sys.stderr)
log_handlers = [stdout_handler]
if config.log.use_file:
    try:
        with open(config.log.file_path, mode='x'):
            pass
    except FileExistsError:
        pass
    file_handler = logging.FileHandler(config.log.file_path)
    log_handlers.append(file_handler)
# noinspection PyArgumentList
logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=config.log.level,
                    handlers=log_handlers)
logging.log(config.log.level, f'\n{config!r}')

event_loop = asyncio.get_event_loop()
proxy_url = None
proxy_auth = None
if config.app.use_proxy:
    proxy_url = config.proxy.url
    if len(config.proxy.username) > 0:
        proxy_auth = aiohttp.BasicAuth(login=config.proxy.username,
                                       password=config.proxy.password)
bot = Bot(token=config.app.token,
          loop=event_loop,
          proxy=proxy_url,
          proxy_auth=proxy_auth)
dispatcher = Dispatcher(bot,
                        loop=event_loop,
                        storage=RedisStorage2(config.redis.host,
                                              config.redis.port,
                                              db=config.redis.db,
                                              prefix=config.redis.prefix))
dispatcher.middleware.setup(LoggingMiddleware())


async def on_startup(dp: aiogram.Dispatcher):
    if config.app.webhook_mode:
        await dp.bot.set_webhook(config.webhook.url)

    me = await dp.bot.get_me()
    logging.warning(f'Powering up @{me["username"]}')


async def on_shutdown(dp: aiogram.Dispatcher):
    logging.warning('Shutting down..')

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    if config.app.webhook_mode:
        await dp.bot.delete_webhook()

    logging.warning('Bye!')


from app.middlewares import trace


@trace
def terminate(signalnum, frame):
    logging.warning(f'!! received {signalnum}, terminating the process')
    sys.exit()


def run():
    from app.dialogue.handlers import register_message_handlers
    register_message_handlers()
    signal.signal(signal.SIGTERM, terminate)
    if config.app.webhook_mode:
        executor.start_webhook(dispatcher=dispatcher,
                               webhook_path=config.webhook.path,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               skip_updates=False,
                               host=config.webhook.webapp_host,
                               port=config.webhook.webapp_port)
    else:
        executor.start_polling(dispatcher,
                               on_startup=on_startup,
                               on_shutdown=on_shutdown,
                               timeout=20)
