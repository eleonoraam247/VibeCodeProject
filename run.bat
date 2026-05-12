@echo off
REM Скрипт для быстрого запуска Vibe Chat на Windows

echo ========================================
echo   Vibe Chat - Быстрый запуск
echo ========================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не установлен или не в PATH
    pause
    exit /b 1
)

REM Создание виртуального окружения если не существует
if not exist "backend\venv" (
    echo [1/4] Создание виртуального окружения...
    cd backend
    python -m venv venv
    cd ..
) else (
    echo [1/4] Виртуальное окружение уже существует
)

REM Активация виртуального окружения
echo [2/4] Активация виртуального окружения...
call backend\venv\Scripts\activate.bat

REM Установка зависимостей
echo [3/4] Установка зависимостей...
cd backend
pip install -r requirements.txt --quiet
cd ..

REM Запуск сервера
echo [4/4] Запуск FastAPI сервера...
echo.
echo ========================================
echo   Сервер запущен на: http://localhost:8000
echo   Документация: http://localhost:8000/docs
echo ========================================
echo.
echo Откройте frontend на: http://localhost:8080
echo Нажмите Ctrl+C для остановки сервера
echo.

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
