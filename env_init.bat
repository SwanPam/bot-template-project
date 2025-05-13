@echo off
REM Название виртуального окружения
set VENV_NAME=venv

REM Создание виртуального окружения
python -m venv %VENV_NAME%

REM Активация виртуального окружения
call %VENV_NAME%\Scripts\activate.bat

REM Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

echo Готово!
pause
