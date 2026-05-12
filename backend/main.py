from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User, Message
import crud
import schemas

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI приложения
app = FastAPI(
    title="Chat API",
    description="REST API для чат-приложения Vibe Coding",
    version="1.0.0"
)

# Настройка CORS для взаимодействия с frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================== API INFO ========================

@app.get("/api", tags=["Root"])
def read_root():
    """Краткая информация об API (UI отдаётся из / как статический frontend)"""
    return {
        "message": "Добро пожаловать в Chat API!",
        "version": "1.0.0",
        "docs": "/docs"
    }


# ======================== USERS ENDPOINTS ========================

@app.post("/users", response_model=schemas.UserResponse, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя"""
    try:
        # Проверка на уникальность username
        db_user = crud.get_user_by_username(db, username=user.username.strip())
        if db_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
        
        # Проверка на уникальность email
        db_user_email = db.query(User).filter(User.email == user.email.lower()).first()
        if db_user_email:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
        
        # Создание пользователя
        new_user = crud.create_user(db=db, user=user)
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Ошибка при создании пользователя: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


@app.get("/users", response_model=list[schemas.UserResponse], tags=["Users"])
def get_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Получить всех пользователей"""
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserDetailResponse, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получить информацию о конкретном пользователе"""
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user


@app.get("/users/search/{query}", response_model=list[schemas.UserResponse], tags=["Users"])
def search_users(query: str, db: Session = Depends(get_db)):
    """Поиск пользователей по имени или email"""
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Строка поиска не может быть пустой")
    
    users = crud.search_users(db, query=query)
    return users


@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя"""
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Пользователь успешно удалён"}


# ======================== MESSAGES ENDPOINTS ========================

@app.post("/messages", response_model=schemas.MessageResponse, tags=["Messages"])
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    """Отправить новое сообщение"""
    # Проверка существования отправителя и получателя
    sender = crud.get_user(db, user_id=message.sender_id)
    receiver = crud.get_user(db, user_id=message.receiver_id)
    
    if not sender:
        raise HTTPException(status_code=404, detail="Отправитель не найден")
    if not receiver:
        raise HTTPException(status_code=404, detail="Получатель не найден")
    
    if message.sender_id == message.receiver_id:
        raise HTTPException(status_code=400, detail="Нельзя отправить сообщение самому себе")
    
    return crud.create_message(db=db, message=message)


@app.get("/messages", response_model=list[schemas.MessageDetailResponse], tags=["Messages"])
def get_messages(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Получить все сообщения"""
    messages = crud.get_all_messages(db, skip=skip, limit=limit)
    return messages


@app.get("/messages/{message_id}", response_model=schemas.MessageDetailResponse, tags=["Messages"])
def get_message(message_id: int, db: Session = Depends(get_db)):
    """Получить конкретное сообщение"""
    db_message = crud.get_message(db, message_id=message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")
    return db_message


@app.get("/messages/conversation/{user1_id}/{user2_id}", response_model=list[schemas.MessageDetailResponse], tags=["Messages"])
def get_conversation(user1_id: int, user2_id: int, db: Session = Depends(get_db)):
    """Получить переписку между двумя пользователями"""
    user1 = crud.get_user(db, user_id=user1_id)
    user2 = crud.get_user(db, user_id=user2_id)
    
    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="Один из пользователей не найден")
    
    return crud.get_conversation(db, user1_id=user1_id, user2_id=user2_id)


@app.get("/messages/search/{query}", response_model=list[schemas.MessageDetailResponse], tags=["Messages"])
def search_messages(query: str, db: Session = Depends(get_db)):
    """Поиск сообщений по содержимому"""
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Строка поиска не может быть пустой")
    
    messages = crud.search_messages(db, query=query)
    return messages


@app.get("/users/{user_id}/messages", response_model=list[schemas.MessageDetailResponse], tags=["Messages"])
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    """Получить все сообщения, отправленные конкретным пользователем"""
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    return crud.get_messages_by_user(db, user_id=user_id)


@app.delete("/messages/{message_id}", tags=["Messages"])
def delete_message(message_id: int, db: Session = Depends(get_db)):
    """Удалить сообщение"""
    success = crud.delete_message(db, message_id=message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Сообщение не найдено")
    return {"message": "Сообщение успешно удалено"}


# ======================== STATISTICS ENDPOINT ========================

@app.get("/stats", tags=["Stats"])
def get_stats(db: Session = Depends(get_db)):
    """Получить статистику по чату"""
    users_count = db.query(User).count()
    messages_count = db.query(Message).count()
    
    return {
        "users_count": users_count,
        "messages_count": messages_count,
        "api_version": "1.0.0"
    }


# Статический frontend (один сервис на Railway/Render: и UI, и API)
_frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if _frontend_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
