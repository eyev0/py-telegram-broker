import json
import logging
import sys

from aiogram.contrib.fsm_storage.redis import RedisStorage2

from app import config

APP_NAME = 'magicproxybot'


class Config(object):

    def __init__(self, container, test_env):
        self.container = container
        self.test_env = test_env

        if self.container:
            self.vol_path = '/vol'
        else:
            self.vol_path = f'/home/egor/{APP_NAME}'
            if self.test_env:
                self.vol_path = self.vol_path + '/test'

        self.config_path = self.vol_path + '/config.json'
        self.proxy_path = self.vol_path + '/proxy.json'
        self.log_path = self.vol_path + f'/{APP_NAME}.log'
        self.states_storage = RedisStorage2(host='localhost',
                                            port=34343,
                                            db='db0',
                                            prefix='fsm')

        self.db_dialect = 'postgres'
        self.db_user = 'docker'
        self.db_password = 'docker'
        self.db_name = 'docker'
        if self.container:
            self.db_host = 'postgres-' + APP_NAME
            self.db_port = '5432'
        else:
            self.db_host = 'localhost'
            self.db_port = '34343'

        self.db_connect_string = self.db_dialect + '://' + self.db_user + ':' + self.db_password + '@' \
            + self.db_host + ':' + self.db_port + '/' + self.db_name

        with open(self.config_path, 'rb') as f:
            self.conf = json.load(f)
            self.TOKEN = self.conf['TOKEN']
            self.admin_ids = self.conf['admin_ids']

        with open(self.proxy_path, 'rb') as f:
            self.proxy_conf = json.load(f)
            self.PROXY_PROTOCOL = self.proxy_conf['protocol']
            self.PROXY_IP = self.proxy_conf['ip']
            self.PROXY_PORT = self.proxy_conf['port']
            self.PROXY_URL = self.PROXY_PROTOCOL + '://' + self.PROXY_IP + ':' + self.PROXY_PORT

    def __repr__(self):
        return f'Config(container={self.container}, test_env={self.test_env}, TOKEN={self.TOKEN}, ' \
               f'PROXY_URL={self.PROXY_URL}, vol_dir={self.vol_path}, admin_ids={self.admin_ids})'


formatter = logging.Formatter(u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s')


def setup_logger(name, file=None, level=logging.INFO):
    if file is not None:
        handler = logging.FileHandler(file)
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


file_logger = setup_logger('file logger', config.log_path, level=logging.INFO)
stdout_logger = setup_logger('stdout_logger', None, level=logging.WARNING)


def log_message(message, level=logging.INFO):
    file_logger.log(level=level, msg=message)
    stdout_logger.log(level=level, msg=message)
