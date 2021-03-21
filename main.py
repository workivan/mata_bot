import asyncio
import logging

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.handlers.user import register_handlers_user
from app.handlers.admin import register_handlers_admin
from app.handlers.data import register_handlers_data
from app.handlers.register import register_handlers_register
from app.handlers.common import register_handlers_common
from app.handlers.test import register_handlers_test
from app.config import *
from app.user import User

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    super_user = User(SUPER_USER_NICKNAME, SUPER_USER_LOGIN, True, False, True, True)
    if not DEBUG:
        await USERS.set_conn(user=os.getenv("DB_USER"),
                             port=os.getenv("DB_PORT"),
                             host=os.getenv("DB_HOST"),
                             database=os.getenv("DB_NAME"),
                             password=os.getenv("DB_PASSWORD")
                             )
    await USERS.update({SUPER_USER_ID: super_user})

    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_admin(dp)
    register_handlers_user(dp)
    register_handlers_data(dp)
    register_handlers_register(dp)
    register_handlers_common(dp)
    register_handlers_test(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())
