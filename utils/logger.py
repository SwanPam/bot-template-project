import logging
import os

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.propagate = False
    if not logger.handlers:  # Чтобы не добавлять несколько обработчиков
        logger.setLevel(logging.INFO)

        # Создание директории logs, если нет
        os.makedirs("logs", exist_ok=True)

        # Файл логов
        file_handler = logging.FileHandler("logs/bot.log", encoding='utf-8')
        file_handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s"))

        # Вывод в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s"))

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
