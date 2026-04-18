from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Email пользователя", example="user@example.com")
    full_name: Optional[str] = Field(None, description="Полное имя", example="Иван Петров")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Пароль", example="strongpass123")


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int = Field(..., description="ID пользователя", example=1)
    is_active: bool = Field(True, description="Активен ли пользователь")

    class Config:
        orm_mode = True