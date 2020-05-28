import argparse
import asyncio
import logging
import sys
from datetime import datetime

import pytz
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from app.config import Config, APP_NAME
from app.decorate_log import LVL_CALL
from app.storage_util import FSMContextFactory

clock = datetime(2020, 1, 1, tzinfo=pytz.timezone('Europe/Moscow'))

parser = argparse.ArgumentParser(description=f'Power up {APP_NAME}. Use -t for testing')
parser.add_argument('-t', '--test', dest='test_env',
                    action='store_true', default=False)
parser.add_argument('-c', '--container', dest='container',
                    action='store_true', default=False)
parser.add_argument('-w', '--webhook', dest='webhook_mode',
                    action='store_true', default=False)
parser.add_argument('-p', '--proxy', dest='proxy',
                    action='store_true', default=False)
args = parser.parse_args()
config = Config(args.container,
                args.test_env,
                args.webhook_mode,
                args.proxy)

file_handler = logging.FileHandler(config.log_file)
stdout_handler = logging.StreamHandler(sys.stderr)
# noinspection PyArgumentList
logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=LVL_CALL,
                    handlers=(file_handler, stdout_handler,))

event_loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, loop=event_loop, proxy=config.PROXY_URL, proxy_auth=config.PROXY_AUTH)
dp = Dispatcher(bot, loop=event_loop, storage=config.states_storage)
dp.middleware.setup(LoggingMiddleware())

import app.db
import app.handlers
