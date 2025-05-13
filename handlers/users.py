from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from utils.logger import setup_logger

logger = setup_logger(__name__)

router = Router()

@router.message(Command("start"))
async def user_handler(message: Message):
    await message.answer(text='Привет')

