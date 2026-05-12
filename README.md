# Vibe Chat — Vibe Coding Final Project

## Short description

A chat-style web app where users register, browse a user list, and exchange messages with full conversation history. The backend is **FastAPI + SQLAlchemy + SQLite**; the frontend is **HTML, CSS, and vanilla JavaScript**. Built as the final project for the **Vibe Coding** course.

---

## Live website

**Replace this with your deployed URL after you publish on Railway, Render, or similar.**

- Example format: `https://your-service.up.railway.app`
- **Live demo:** *[paste your URL here]*

Swagger for the API (when deployed): `{your-deployed-origin}/docs`

---

## YouTube demo video

**Paste the link to your walkthrough/demo video.**

- **Demo:** *[https://www.youtube.com/watch?v=YOUR_VIDEO_ID](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)*

---

## Screenshots

Demo capture (hosted on GitHub):

![Vibe Chat — main interface](https://github.com/user-attachments/assets/a1bb41e4-bfee-4639-a295-74098336eb0a)

You can also add images under `docs/screenshots/` in this repo:

<!--
![Main interface](docs/screenshots/main.png)
![Chat view](docs/screenshots/chat.png)
-->

---

## Features

### User management

- Register users (username + email)
- List all users
- Search users by name or email

### Messaging

- Send messages between two users
- Load conversation history for a pair of users
- Optional search endpoints for messages (API)

### Interface

- Sidebar with users and stats counter
- Chat panel with messages and emoji picker input
- Dark-themed layout

### Backend

- REST API (FastAPI)
- Automatic OpenAPI docs at `/docs` when the API is running
- SQLite persistence

---

## Tech stack

| Layer      | Technologies                          |
|-----------|----------------------------------------|
| Backend   | Python, FastAPI, Uvicorn, SQLAlchemy  |
| Database  | SQLite                                 |
| Frontend  | HTML, CSS, JavaScript                  |
| Deploy    | Railway / Render (see `Procfile`, `railway.json`) |

---

## How to run locally

You need **two terminals**: one for the API, one to serve static files (so the frontend can detect the backend and avoid `file://` issues).

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- API base: **http://127.0.0.1:8000**
- Docs: **http://127.0.0.1:8000/docs**

### 2. Frontend

```bash
cd frontend
python -m http.server 8080
```

Open **http://127.0.0.1:8080** in your browser. The frontend tries to resolve the API (including common local ports).

### Prerequisites

- Python **3.8+**
- Git (optional)

---

## Project structure

```
chat-app/
│
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── crud.py              # Create, Read, Update, Delete operations
│   ├── requirements.txt     # Python dependencies
│   └── chat.db              # SQLite database file (created at runtime)
│
├── frontend/
│   ├── index.html           # Main HTML template
│   ├── style.css            # CSS styling
│   └── app.js               # JavaScript functionality
│
├── README.md                # Project documentation
└── .gitignore               # Git ignore rules
```

---

## API endpoints (summary)

### Users

- `GET /users` — list users
- `POST /users` — create user
- `GET /users/{user_id}` — user detail
- `GET /users/search/{query}` — search users

### Messages

- `GET /messages` — list messages
- `POST /messages` — send message
- `GET /messages/{message_id}` — one message
- `GET /messages/conversation/{user1_id}/{user2_id}` — conversation between two users
- `GET /messages/search/{query}` — search message text

Full interactive docs: `/docs` on the running server.

---

## Usage

1. **Create a user** in the left panel (this becomes “you”).
2. **Click another user** to open the chat.
3. **Send messages**; history loads from the API.

---

## Database schema

### Users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Messages

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
)
```

---

## Deployment

### Railway

See [DEPLOYMENT_RAILWAY.md](DEPLOYMENT_RAILWAY.md) for step-by-step instructions.

### Render

Create a Web Service, connect this repository, install dependencies from `requirements.txt`, and run Uvicorn similarly to `Procfile`.

---

## Future enhancements

- Real-time messaging (WebSockets)
- Authentication and sessions
- Group chats

---

## License

This project is part of the Vibe Coding course. All rights reserved.

---

## Acknowledgments

- Vibe Coding for the course and guidance
- [FastAPI](https://fastapi.tiangolo.com/) documentation and community
- [SQLAlchemy](https://www.sqlalchemy.org/)
- All contributors and testers
