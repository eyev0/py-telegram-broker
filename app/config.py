import ast
import os
from pathlib import Path

import aiohttp
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from app.decorate_log import LVL_CALL

APP_NAME = 'salesboard'


class Config:

    class DBConfig:
        def __init__(self, container, test_env):
            self.db_dialect = 'postgres'
            self.db_user = 'docker'
            self.db_password = 'docker'
            self.db_name = 'docker'
            if container:
                self.db_host = 'db'
                self.db_port = '5432'
            else:
                self.db_host = 'localhost'
                self.db_port = '45432'

            self.db_connect_string = self.db_dialect + '://' + self.db_user + ':' + self.db_password + '@' \
                + self.db_host + ':' + self.db_port + '/' + self.db_name

    class RedisConfig:
        def __init__(self, container, test_env):
            if container:
                self.redis_host = 'redis'
                self.redis_port = '6379'
            else:
                self.redis_host = 'localhost'
                self.redis_port = '46379'

            if test_env:
                prefix = 'test'
            else:
                prefix = ''
            self.states_storage = RedisStorage2(host=self.redis_host,
                                                port=self.redis_port,
                                                db=0,
                                                prefix=f'{prefix}fsm')

    class LogConfig:
        def __init__(self, container, test_env):
            if container:
                self.log_path = '/log'
            else:
                self.log_path = f'{Path(os.path.dirname(__file__)).parent}/data/log'
            if test_env:
                self.log_file = self.log_path + f'/{APP_NAME}-test.log'
            else:
                self.log_file = self.log_path + f'/{APP_NAME}.log'
            self.log_level = LVL_CALL

    class ProxyConfig:
        def __init__(self, use_proxy):
            if use_proxy:
                proxy_conf = ast.literal_eval(os.environ[f'{APP_NAME.upper()}_PROXY'])
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

    class WebhookConfig:
        def __init__(self, webhook_mode, token=None):
            if webhook_mode:
                webhook_conf = ast.literal_eval(os.environ[f'{APP_NAME.upper()}_WEBHOOK'])
                self.WEBHOOK_HOST = webhook_conf['host']
                self.WEBHOOK_PORT = webhook_conf['port']
                self.WEBHOOK_PATH = f'/{token}'
                self.WEBHOOK_URL = f'https://{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}'

                # webserver settings
                self.WEBAPP_HOST = '0.0.0.0'  # or ip
                self.WEBAPP_PORT = int(self.WEBHOOK_PORT)

    def __init__(self, container, test_env, webhook_mode, use_proxy):

        self.TOKEN = os.environ[f'{APP_NAME.upper()}_TOKEN']
        self.check_admin = ast.literal_eval(os.environ[f'{APP_NAME.upper()}_ADMINS'])
        self.admins = []
        self.db = self.__class__.DBConfig(container, test_env)
        self.redis = self.__class__.RedisConfig(container, test_env)
        self.log = self.__class__.LogConfig(container, test_env)
        self.proxy = self.__class__.ProxyConfig(use_proxy)
        self.webhook_mode = webhook_mode
        self.webhook = self.__class__.WebhookConfig(webhook_mode, self.TOKEN)

    def __repr__(self):
        return f'TOKEN={self.TOKEN}'
