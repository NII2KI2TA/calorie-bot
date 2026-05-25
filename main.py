import os
import asyncio
import threading

from flask import Flask

from aiogram import (
    Bot,
    Dispatcher
)

from aiogram.fsm.storage.memory import (
    MemoryStorage
)

from handlers.user import router


TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_router(router)


app = Flask(__name__)


@app.route("/")
def home():

    return "Bot is running!"


def run_web():

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )


async def run_bot():

    await dp.start_polling(bot)


async def main():

    threading.Thread(
        target=run_web
    ).start()

    await run_bot()


if __name__ == "__main__":

    asyncio.run(main())