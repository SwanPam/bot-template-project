@echo off
REM Название виртуального окружения
set VENV_NAME=venv

REM Активация виртуального окружения
call %VENV_NAME%\Scripts\activate.bat

REM Установка необходимых пакетов
pip install alembic
pip install psycopg2-binary
pip install sqlalchemy
pip install asyncpg

REM Инициализация Alembic
alembic init alembic

echo Готово!
pause
