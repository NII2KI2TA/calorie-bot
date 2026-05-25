import asyncio

from aiogram import (
    Bot,
    Dispatcher
)

from aiogram.fsm.storage.memory import (
    MemoryStorage
)

from handlers.user import router


import os

TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(
    storage=storage
)

dp.include_router(router)


async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())