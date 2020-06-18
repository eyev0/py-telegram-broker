from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loguru import logger


class LoguruLoggingMiddleware(LoggingMiddleware):
    def __init__(self):
        self.logger = logger
        super(LoggingMiddleware, self).__init__()
