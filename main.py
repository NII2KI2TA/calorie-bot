import os
import asyncio
from threading import Thread

from flask import Flask

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from handlers.user import router


TOKEN = os.getenv("BOT_TOKEN")

session = AiohttpSession()

bot = Bot(
    token=TOKEN,
    session=session
)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_router(router)


# FLASK

app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running!"


def run_web():
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )


# BOT

async def run_bot():

    print("BOT STARTED")

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(bot)


# MAIN

if __name__ == "__main__":

    web_thread = Thread(
        target=run_web
    )

    web_thread.start()

    asyncio.run(run_bot())