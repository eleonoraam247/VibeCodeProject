# 🚀 Развёртывание на Railway

## Шаг 1: Создайте GitHub репозиторий

1. Откройте https://github.com/new
2. Создайте новый репозиторий с именем `vibe-chat`
3. Выберите "Public"
4. Нажмите "Create repository"

---

## Шаг 2: Загрузите код на GitHub

```bash
# В папке проекта VibeCodeProject

git add .
git commit -m "Initial commit - Vibe Chat Project"
git branch -M main
git remote add origin https://github.com/ВАШ_GITHUB_ИМЕЕТ/vibe-chat.git
git push -u origin main
```

**Замените:** `ВАШ_GITHUB_ИМЕЕТ` на ваше реальное имя GitHub!

---

## Шаг 3: Развёртывание на Railway

1. Откройте https://railway.app
2. Нажмите **"Login"** (зарегистрируйтесь если нужно)
3. Выберите **"New Project"**
4. Выберите **"Deploy from GitHub"**
5. Подключите GitHub аккаунт
6. Выберите репозиторий **`vibe-chat`**
7. Нажмите **"Deploy"**

Railway автоматически:
- 🔄 Установит зависимости из `requirements.txt`
- 🚀 Запустит приложение через `Procfile`
- 🌐 Выдаст вам публичный URL

---

## Шаг 4: Получите публичный URL

После развёртывания Railway выдаст вам ссылку типа:
```
https://vibe-chat-production.up.railway.app
```

**Backend API будет доступен на:**
```
https://vibe-chat-production.up.railway.app
```

**API документация:**
```
https://vibe-chat-production.up.railway.app/docs
```

---

## Шаг 5: Обновите Frontend

Измените `API_BASE_URL` в `frontend/app.js`:

```javascript
// Было:
const API_BASE_URL = 'http://localhost:8000';

// Стало:
const API_BASE_URL = 'https://vibe-chat-production.up.railway.app';
```

Или сделайте его динамическим:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000'
  : 'https://vibe-chat-production.up.railway.app';
```

---

## ✅ Готово!

Ваш проект теперь на облаке! 🎉

---

## 🔗 Полезные ссылки

- Railway Dashboard: https://railway.app/dashboard
- GitHub Settings: https://github.com/settings
- Railway Docs: https://docs.railway.app

---

## 🆘 Если что-то не работает

**Проверьте логи на Railway:**
1. Откройте проект на https://railway.app
2. Перейдите на вкладку "Logs"
3. Посмотрите ошибки

**Общие проблемы:**
- Port не совпадает → Railway автоматически передаёт PORT через $PORT ✅
- БД не создана → SQLite создаётся автоматически ✅
- Зависимости не установлены → requirements.txt установиться автоматически ✅
