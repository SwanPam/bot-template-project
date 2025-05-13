from aiogram.filters import Command
from aiogram import Router


router = Router()

@router.message(Command("admin"))
async def admin_handler(msg):
    await msg.answer("Admin only")
