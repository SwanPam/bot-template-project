from database.engine import engine
from database.models import Base
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect

from utils.logger import setup_logger


logger = setup_logger(__name__)


async def check_tables_exist() -> bool:
    try:
        async with engine.connect() as conn:
            result = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
            logger.info("Проверка наличия таблиц прошла успешно.")
            return bool(result)  
    except OperationalError:
        return False  

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы успешно созданы.")


async def setup_db():
    if not await check_tables_exist():
        logger.info("Таблицы не найдены. Создаю...")
        await init_db()
    else:
        logger.info("Таблицы уже существуют. Пропускаю создание.")
        