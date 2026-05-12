#!/bin/bash

# Скрипт для быстрого запуска Vibe Chat на Linux/Mac

echo "========================================"
echo "   Vibe Chat - Быстрый запуск"
echo "========================================"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python3 не установлен"
    exit 1
fi

# Создание виртуального окружения если не существует
if [ ! -d "backend/venv" ]; then
    echo "[1/4] Создание виртуального окружения..."
    cd backend
    python3 -m venv venv
    cd ..
else
    echo "[1/4] Виртуальное окружение уже существует"
fi

# Активация виртуального окружения
echo "[2/4] Активация виртуального окружения..."
source backend/venv/bin/activate

# Установка зависимостей
echo "[3/4] Установка зависимостей..."
cd backend
pip install -r requirements.txt --quiet
cd ..

# Запуск сервера
echo "[4/4] Запуск FastAPI сервера..."
echo ""
echo "========================================"
echo "   Сервер запущен на: http://localhost:8000"
echo "   Документация: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "Откройте frontend на: http://localhost:8080"
echo "Нажмите Ctrl+C для остановки сервера"
echo ""

cd backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
