# Vibe Coding Final Project — Chat Website

A simple real-time style chat website built with Python FastAPI for the backend and HTML/CSS/JavaScript for the frontend.

## Project Description

This application allows users to communicate with each other through a clean, modern web interface. The chat system features user management, real-time messaging, and complete chat history viewing.

The project was developed as a final project for the Vibe Coding course.

---

## Features

### User Management
- ✅ Add/Register users
- ✅ Display all users
- ✅ Search users by username

### Messaging System
- ✅ Send messages between users
- ✅ Receive messages
- ✅ View complete chat history
- ✅ Search messages
- ✅ Show conversation between two users

### Frontend
- ✅ Simple responsive UI
- ✅ User list panel
- ✅ Chat window
- ✅ Message input
- ✅ Dark mode design

### Backend
- ✅ REST API using FastAPI
- ✅ API endpoints for users and messages
- ✅ JSON data handling
- ✅ Swagger API documentation at `/docs`

### Database
- ✅ SQLite database for storing:
  - Users
  - Messages

---

## Tech Stack

### Backend
- **Python** - Programming language
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database

### Frontend
- **HTML** - Markup language
- **CSS** - Styling and layout
- **JavaScript** - Client-side interactivity

### Deployment
- **Railway** / **Render** - Cloud deployment platforms

### Version Control
- **GitHub** - Repository hosting

---

## Project Structure

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
│   └── chat.db              # SQLite database file
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

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js (optional, for frontend development)
- Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

The backend will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Open the frontend directory:
   ```bash
   cd frontend
   ```

2. Open `index.html` in your web browser or serve it using a local server:
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js (if installed)
   npx http-server
   ```

The frontend will be available at `http://localhost:8080`

---

## API Endpoints

### Users
- `GET /users` - Get all users
- `POST /users` - Create a new user
- `GET /users/{user_id}` - Get a specific user
- `GET /users/search/{username}` - Search users by username

### Messages
- `GET /messages` - Get all messages
- `POST /messages` - Send a new message
- `GET /messages/{message_id}` - Get a specific message
- `GET /messages/conversation/{user1_id}/{user2_id}` - Get conversation between two users
- `GET /messages/search/{query}` - Search messages

---

## Usage

1. **Register Users:** Use the frontend to create new user accounts
2. **View Users:** See all registered users in the user list panel
3. **Send Messages:** Select a user and type your message in the input field
4. **View Chat History:** All messages are displayed in the chat window
5. **Search:** Use search functionality to find users or specific messages

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Messages Table
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

### Deploy to Railway
1. Create a Railway account at [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Set environment variables as needed
4. Deploy from the Railway dashboard

### Deploy to Render
1. Create a Render account at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure build and start commands
5. Deploy

---

## Future Enhancements

- [ ] Real-time messaging with WebSockets
- [ ] User authentication and login
- [ ] Message encryption
- [ ] Group chat functionality
- [ ] File sharing capabilities
- [ ] Typing indicators
- [ ] Message reactions/emojis
- [ ] User profile customization
- [ ] Mobile-responsive improvements
- [ ] Push notifications

---

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any improvements.

---

## License

This project is part of the Vibe Coding course. All rights reserved.

---

## Contact & Support

For questions or support regarding this project, please reach out through the Vibe Coding course platform.

---

## Acknowledgments

- Vibe Coding for the course and guidance
- FastAPI documentation and community
- SQLAlchemy for excellent ORM capabilities
- All contributors and testers

---
