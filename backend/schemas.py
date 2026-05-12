from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    username: str = Field(..., min_length=1, max_length=255, description="Имя пользователя")
    email: str = Field(..., description="Email пользователя")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('Некорректный формат email')
        return v.lower()
    
    @validator('username')
    def validate_username(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Имя пользователя не может быть пустым')
        return v


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    pass


class UserResponse(UserBase):
    """Схема ответа пользователя"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    """Базовая схема сообщения"""
    sender_id: int
    receiver_id: int
    content: str


class MessageCreate(MessageBase):
    """Схема для создания сообщения"""
    pass


class MessageResponse(MessageBase):
    """Схема ответа сообщения"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MessageDetailResponse(MessageResponse):
    """Детальная схема ответа сообщения с информацией об отправителе и получателе"""
    sender: UserResponse
    receiver: UserResponse

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """Детальная схема пользователя с сообщениями"""
    sent_messages: List[MessageResponse] = []
    received_messages: List[MessageResponse] = []

    class Config:
        from_attributes = True
