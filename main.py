import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from handlers.user import router


# TOKEN

TOKEN = os.getenv("BOT_TOKEN")


# SESSION

session = AiohttpSession()


# BOT

bot = Bot(
    token=TOKEN,
    session=session
)


# STORAGE

storage = MemoryStorage()


# DISPATCHER

dp = Dispatcher(storage=storage)

dp.include_router(router)


# START BOT

async def main():

    print("BOT STARTED")

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(bot)


# MAIN

if __name__ == "__main__":

    asyncio.run(main())