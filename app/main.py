from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.config import settings

# Создание приложения
if settings.ENVIRONMENT == "production":
    app = FastAPI(
        title="SPA Salon API",
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )
else:
    app = FastAPI(
        title="SPA Salon API — Лабораторная работа №4",
        description="""
        ## Автоматизированное документирование REST API с использованием OpenAPI (Swagger)

        Данное API предоставляет функционал для SPA-салона:
        * **Аутентификация** (JWT в HttpOnly cookies)
        * **Регистрация пользователей**
        * **Управление пользователями**

        ### Технологии:
        * FastAPI
        * JWT (HttpOnly cookies)
        * PostgreSQL

        ### Безопасность:
        * Для защищённых эндпоинтов требуется авторизация.
        """,
        summary="REST API для SPA-салона с автодокументацией",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )


# ========== МОДЕЛИ ДАННЫХ ==========
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class MessageResponse(BaseModel):
    message: str


# ========== ВРЕМЕННАЯ БАЗА ДАННЫХ ==========
users_db = {}


# ========== ЭНДПОИНТЫ ==========

@app.post("/api/v1/auth/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister):
    """Регистрация нового пользователя"""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.email] = {
        "email": user.email,
        "password": user.password,
        "full_name": user.full_name
    }

    return MessageResponse(message=f"User {user.email} registered successfully")


@app.post("/api/v1/auth/login", response_model=MessageResponse)
async def login_user(user: UserLogin, response: Response):
    """Вход в систему"""
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if users_db[user.email]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response.set_cookie(
        key="access_token",
        value="fake-jwt-token-for-demo",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        path="/"
    )

    return MessageResponse(message="Login successful")


@app.post("/api/v1/auth/logout", response_model=MessageResponse)
async def logout_user(response: Response):
    """Выход из системы"""
    response.delete_cookie("access_token", path="/")
    return MessageResponse(message="Logout successful")


@app.get("/api/v1/auth/me")
async def get_current_user():
    """Получить информацию о текущем пользователе"""
    return {"message": "Current user info - implement with real token"}


@app.get("/api/v1/users/")
async def get_users():
    """Список пользователей"""
    return list(users_db.values())


@app.get("/")
async def root():
    return {
        "message": "SPA Salon API",
        "environment": settings.ENVIRONMENT,
        "docs": "/api/docs" if settings.ENVIRONMENT != "production" else "disabled",
        "users_count": len(users_db)
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}