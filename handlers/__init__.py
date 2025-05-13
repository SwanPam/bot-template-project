from aiogram import Router

from .users import router as user_router
from .admin import router as admin_router

all_handlers = Router()
all_handlers.include_router(user_router)
all_handlers.include_router(admin_router)
