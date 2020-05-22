import logging

from aiogram.utils import executor

from app import dp as dispatcher, config
from app.decorate_log import trace_async


@trace_async
async def on_startup(dp):
    me = await dp.bot.get_me()
    logging.warning(f'Powering up @{me["username"]}')
    logging.warning(f'Config is:{config!r}')


@trace_async
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
