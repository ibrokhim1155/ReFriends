import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from db import init_db, conn, cursor


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
HELP_USERNAME = os.getenv("HELP_USERNAME")
GROUP_ID = int(os.getenv("GROUP_ID"))

if not BOT_TOKEN or not ADMIN_ID or not CHANNEL_USERNAME or not HELP_USERNAME or not GROUP_ID:
    raise ValueError("Missing required .env values")


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


init_db()
