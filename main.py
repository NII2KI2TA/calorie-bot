import os
import asyncio

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from handlers.user import router

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("RENDER_URL")

session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

app = FastAPI()


# ---------- STARTUP ----------
@app.on_event("startup")
async def on_startup():
    print("BOT STARTED (FASTAPI WEBHOOK)")

    webhook_url = f"{BASE_URL}/webhook"
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(webhook_url)


# ---------- WEBHOOK ----------
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    update = types.Update(**data)

    await dp.feed_update(bot, update)

    return {"ok": True}


# ---------- HEALTH ----------
@app.get("/")
def home():
    return "Bot is running (FastAPI + webhook)"