import ast
import os
from pathlib import Path

import aiohttp
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from app.decorate_log import LVL_CALL

APP_NAME = 'salesboard'


class Config(object):

    def __init__(self, container, test_env, webhook_mode, proxy):
        self.container = container
        self.test_env = test_env
        self.webhook_mode = webhook_mode
        self.use_proxy = proxy

        if self.container:
            self.log_path = '/log'
        else:
            self.log_path = f'{Path(os.path.dirname(__file__)).parent}/data/log'

        self.log_file = self.log_path + f'/{APP_NAME}{"-test" if test_env else ""}.log'
        self.log_level = LVL_CALL

        self.db_dialect = 'postgres'
        self.db_user = 'docker'
        self.db_password = 'docker'
        self.db_name = 'docker'
        if self.container:
            self.db_host = 'db'
            self.redis_host = 'redis'
            self.db_port = '5432'
            self.redis_port = '6379'
        else:
            self.db_host = self.redis_host = 'localhost'
            self.db_port = '45432'
            self.redis_port = '46379'

        self.db_connect_string = self.db_dialect + '://' + self.db_user + ':' + self.db_password + '@' \
            + self.db_host + ':' + self.db_port + '/' + self.db_name

        if test_env:
            prefix = 'test'
        else:
            prefix = ''
        self.states_storage = RedisStorage2(host=self.redis_host,
                                            port=self.redis_port,
                                            db=0,
                                            prefix=f'{prefix}fsm')

        self.TOKEN = os.environ['SALESBOARD_TOKEN']
        self.check_admin = ast.literal_eval(os.environ['SALESBOARD_ADMIN'])
        self.admins = []

        if self.use_proxy:
            proxy_conf = ast.literal_eval(os.environ['SALESBOARD_PROXY'])
            self.PROXY_PROTOCOL = proxy_conf['protocol']
            self.PROXY_IP = proxy_conf['ip']
            self.PROXY_PORT = proxy_conf['port']
            self.PROXY_USERNAME = proxy_conf['username'] or ''
            self.PROXY_PASSWD = proxy_conf['password'] or ''
            self.PROXY_URL = self.PROXY_PROTOCOL + '://' + self.PROXY_IP + ':' + self.PROXY_PORT

            if len(self.PROXY_USERNAME) > 0:
                self.PROXY_AUTH = aiohttp.BasicAuth(login=self.PROXY_USERNAME, password=self.PROXY_PASSWD)
            else:
                self.PROXY_AUTH = None
        else:
            self.PROXY_URL = None
            self.PROXY_AUTH = None

        if self.webhook_mode:
            webhook_conf = ast.literal_eval(os.environ['SALESBOARD_WEBHOOK'])
            self.WEBHOOK_HOST = webhook_conf['host']
            self.WEBHOOK_PATH = f'/{self.TOKEN}'
            self.WEBHOOK_URL = f'{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}'

            # webserver settings
            self.WEBAPP_HOST = 'localhost'  # or ip
            self.WEBAPP_PORT = 3001

    def __repr__(self):
        return f'Config(container={self.container}, test_env={self.test_env}, TOKEN={self.TOKEN}, ' \
               f'PROXY_URL={self.PROXY_URL})'
