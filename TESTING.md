# API Testing Guide - Руководство по тестированию API

## Быстрый старт

### 1. Установка и запуск Backend

```bash
# Перейти в папку backend
cd backend

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn main:app --reload
```

Сервер будет доступен на: **http://localhost:8000**
API документация: **http://localhost:8000/docs**

---

### 2. Запуск Frontend

```bash
# В отдельном терминале, перейти в frontend
cd frontend

# Запустить локальный веб-сервер (Windows)
python -m http.server 8080

# Или если установлен Node.js
npx http-server
```

Frontend будет доступен на: **http://localhost:8080**

---

## 🧪 Тестирование API в Swagger UI

1. Откройте http://localhost:8000/docs
2. Вы увидите интерактивную документацию всех endpoints

### Пример тестирования:

#### Шаг 1: Создать пользователя
```json
POST /users
{
  "username": "alice",
  "email": "alice@example.com"
}
```

#### Шаг 2: Создать второго пользователя
```json
POST /users
{
  "username": "bob",
  "email": "bob@example.com"
}
```

#### Шаг 3: Отправить сообщение
```json
POST /messages
{
  "sender_id": 1,
  "receiver_id": 2,
  "content": "Привет, Bob!"
}
```

#### Шаг 4: Получить переписку
```
GET /messages/conversation/1/2
```

#### Шаг 5: Поиск пользователей
```
GET /users/search/ali
```

#### Шаг 6: Получить статистику
```
GET /stats
```

---

## 🔍 Тестирование с помощью curl

### Создать пользователя
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"alice\",\"email\":\"alice@example.com\"}"
```

### Получить всех пользователей
```bash
curl "http://localhost:8000/users"
```

### Отправить сообщение
```bash
curl -X POST "http://localhost:8000/messages" \
  -H "Content-Type: application/json" \
  -d "{\"sender_id\":1,\"receiver_id\":2,\"content\":\"Hello!\"}"
```

### Получить переписку
```bash
curl "http://localhost:8000/messages/conversation/1/2"
```

### Поиск сообщений
```bash
curl "http://localhost:8000/messages/search/hello"
```

---

## 📱 Использование Frontend

1. Откройте http://localhost:8080
2. **Создайте пользователя** (левая панель сверху)
3. **Обновите список** - нажмите "Обновить"
4. **Выберите пользователя** из списка для чата
5. **Напишите сообщение** и нажмите "Отправить"

---

## 🐛 Решение проблем

### Ошибка: "CORS error"
✅ **Решение:** Убедитесь, что backend запущен на `http://localhost:8000`

### Ошибка: "Connection refused"
✅ **Решение:** Проверьте, что сервер FastAPI запущен (`uvicorn main:app --reload`)

### База данных не создаётся
✅ **Решение:** Базу данных создаёт автоматически. Проверьте права доступа к папке `backend/`

### Frontend не показывает пользователей
✅ **Решение:** 
- Проверьте консоль браузера (F12)
- Убедитесь, что API_BASE_URL в app.js = `http://localhost:8000`

---

## 📊 Endpoints Reference

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/` | Информация об API |
| POST | `/users` | Создать пользователя |
| GET | `/users` | Получить всех пользователей |
| GET | `/users/{id}` | Получить пользователя |
| GET | `/users/search/{query}` | Поиск пользователей |
| DELETE | `/users/{id}` | Удалить пользователя |
| POST | `/messages` | Отправить сообщение |
| GET | `/messages` | Получить все сообщения |
| GET | `/messages/{id}` | Получить сообщение |
| GET | `/messages/conversation/{u1}/{u2}` | Получить переписку |
| GET | `/messages/search/{query}` | Поиск сообщений |
| GET | `/users/{id}/messages` | Сообщения пользователя |
| DELETE | `/messages/{id}` | Удалить сообщение |
| GET | `/stats` | Получить статистику |

---

## 🚀 Развёртывание

### Развёртывание на Railway
1. Создайте репозиторий GitHub
2. Загрузите код в репозиторий
3. Подключитесь к Railway через GitHub
4. Установите переменные окружения
5. Развёртывание произойдёт автоматически

### Развёртывание на Render
1. Синхронизируйте код с GitHub
2. Создайте новый Web Service на Render.com
3. Выберите GitHub репозиторий
4. Установите build и start команды
5. Развёртывание произойдёт автоматически

---

**Всё готово для тестирования! 🎉**
