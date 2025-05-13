import asyncio
from server import start_fastapi_server
from bot import start_bot
from database.init_db import setup_db
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def main():
    try:
        await setup_db()
        logger.info("База данных успешно инициализирована.")
        await asyncio.gather(
            asyncio.create_task(start_fastapi_server()),
            asyncio.create_task(start_bot())
        )
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")

if __name__ == "__main__":
    try:
        logger.info("Запуск бота и FastApi сервера.")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot and FastAPI server have been stopped.")
