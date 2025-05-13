from core.core import bot, dp
from handlers import all_handlers
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def start_bot():
    try:
        dp.include_router(all_handlers)
        logger.info("Bot is starting polling.")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error during bot startup: {str(e)}")
