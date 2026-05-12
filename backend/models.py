from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с сообщениями
    sent_messages = relationship(
        "Message", 
        foreign_keys="Message.sender_id",
        back_populates="sender"
    )
    received_messages = relationship(
        "Message", 
        foreign_keys="Message.receiver_id",
        back_populates="receiver"
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Message(Base):
    """Модель сообщения"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Связи с пользователями
    sender = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_messages"
    )
    receiver = relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_messages"
    )

    def __repr__(self):
        return f"<Message(id={self.id}, sender_id={self.sender_id}, receiver_id={self.receiver_id})>"
