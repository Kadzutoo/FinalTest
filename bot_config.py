from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from aiogram.fsm.storage.memory import MemoryStorage

from database import Database

# Получение токена из .env
config = dotenv_values(".env")
bot = Bot(token=config.get("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())

# Подключение базы данных
database = Database("db.sqlite3")
