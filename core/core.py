from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN


bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
