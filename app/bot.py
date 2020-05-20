import logging

from aiogram.utils import executor

from app import dp as dispatcher, config
from app.decorators import log_call


@log_call
async def on_startup(dp):
    logging.warning('Powering up.')
    logging.warning('Config is:' + str(config))


@log_call
async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

if __name__ == '__main__':
    executor.start_polling(dispatcher,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           timeout=20)
