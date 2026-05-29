import os
import asyncio

from flask import Flask, request

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import types

from handlers.user import router

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("RENDER_URL")  # например https://your-app.onrender.com

session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

app = Flask(__name__)


# ---------- WEBHOOK HANDLER ----------

@app.route("/webhook", methods=["POST"])
async def webhook():
    data = await request.get_json()

    update = types.Update(**data)

    await dp.feed_update(bot, update)

    return "ok", 200


# ---------- SET WEBHOOK ----------

async def on_start():
    print("BOT STARTED (WEBHOOK MODE)")

    webhook_url = f"{BASE_URL}/webhook"

    await bot.set_webhook(webhook_url)


# ---------- ROUTE FOR RENDER ----------

@app.route("/")
def home():
    return "Bot is running (webhook mode)!"


# ---------- MAIN ----------

if __name__ == "__main__":

    # запускаем webhook настройку
    asyncio.run(on_start())

    # запускаем Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)