from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import User, Message
import schemas


# ======================== Операции с пользователями ========================

def create_user(db: Session, user: schemas.UserCreate) -> User:
    """Создать нового пользователя"""
    db_user = User(
        username=user.username.strip(),
        email=user.email.lower().strip()
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise Exception(f"Ошибка при создании пользователя: {str(e)}")


def get_user(db: Session, user_id: int) -> User:
    """Получить пользователя по ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User:
    """Получить пользователя по имени"""
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list:
    """Получить всех пользователей"""
    return db.query(User).offset(skip).limit(limit).all()


def search_users(db: Session, query: str) -> list:
    """Поиск пользователей по имени или email"""
    return db.query(User).filter(
        or_(
            User.username.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%")
        )
    ).all()


def delete_user(db: Session, user_id: int) -> bool:
    """Удалить пользователя"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


# ======================== Операции с сообщениями ========================

def create_message(db: Session, message: schemas.MessageCreate) -> Message:
    """Создать новое сообщение"""
    db_message = Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_message(db: Session, message_id: int) -> Message:
    """Получить сообщение по ID"""
    return db.query(Message).filter(Message.id == message_id).first()


def get_all_messages(db: Session, skip: int = 0, limit: int = 100) -> list:
    """Получить все сообщения"""
    return db.query(Message).offset(skip).limit(limit).all()


def get_conversation(db: Session, user1_id: int, user2_id: int) -> list:
    """Получить переписку между двумя пользователями"""
    return db.query(Message).filter(
        or_(
            (Message.sender_id == user1_id) & (Message.receiver_id == user2_id),
            (Message.sender_id == user2_id) & (Message.receiver_id == user1_id)
        )
    ).order_by(Message.created_at).all()


def search_messages(db: Session, query: str) -> list:
    """Поиск сообщений по содержимому"""
    return db.query(Message).filter(
        Message.content.ilike(f"%{query}%")
    ).all()


def get_messages_by_user(db: Session, user_id: int) -> list:
    """Получить все сообщения отправленные определённым пользователем"""
    return db.query(Message).filter(Message.sender_id == user_id).all()


def delete_message(db: Session, message_id: int) -> bool:
    """Удалить сообщение"""
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
        return True
    return False
