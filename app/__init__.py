import argparse
import logging
import sys
from datetime import datetime

import pytz
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from app.config import Config, APP_NAME
from app.log import LVL_CALL
from app.storage_util import FSMContextFactory

clock = datetime(2020, 1, 1, tzinfo=pytz.timezone('Europe/Moscow'))

parser = argparse.ArgumentParser(description=f'Power up {APP_NAME}. Use -t for testing')
parser.add_argument('-t', '--test', dest='test_env',
                    action='store_true', default=False)
parser.add_argument('-c', '--container', dest='container',
                    action='store_true', default=False)
args = parser.parse_args()
config = Config(args.container, args.test_env)

file_handler = logging.FileHandler(config.log_path)
stdout_handler = logging.StreamHandler(sys.stderr)
# noinspection PyArgumentList
logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=LVL_CALL,
                    handlers=(file_handler, stdout_handler,))

bot = Bot(token=config.TOKEN, proxy=config.PROXY_URL)
dp = Dispatcher(bot, storage=config.states_storage)
dp.middleware.setup(LoggingMiddleware())

import app.handlers
