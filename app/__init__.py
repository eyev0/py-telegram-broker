import argparse
from datetime import datetime

import pytz
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from app.config import Config, APP_NAME
from app.storage_util import FSMContextFactory

clock = datetime(2020, 1, 1, tzinfo=pytz.timezone('Europe/Moscow'))

parser = argparse.ArgumentParser(description=f'Power up {APP_NAME}. Use -t for testing')
parser.add_argument('-t', '--test', dest='test_env',
                    action='store_true', default=False)
parser.add_argument('-c', '--container', dest='container',
                    action='store_true', default=False)
args = parser.parse_args()
config = Config(args.container, args.test_env)

bot = Bot(token=config.TOKEN, proxy=config.PROXY_URL)
dp = Dispatcher(bot, storage=JSONStorage(config.FSMstorage_path))
dp.middleware.setup(LoggingMiddleware())

from custom import *
import app.handlers
