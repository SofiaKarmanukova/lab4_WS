from fastapi import FastAPI, HTTPException, status, Response, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from urllib.parse import urlencode
import secrets
import httpx

from app.core.config import settings


# ========== СОЗДАНИЕ ПРИЛОЖЕНИЯ ==========

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
        * **Регистрация пользователей**
        * **Вход пользователей**
        * **Выход пользователей**
        * **OAuth-авторизация через Яндекс**
        * **Просмотр списка пользователей**

        ### Технологии:
        * FastAPI
        * Swagger / OpenAPI
        * JWT / Cookies
        * Yandex OAuth
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
oauth_states = set()


# ========== ОБЫЧНАЯ РЕГИСТРАЦИЯ И ВХОД ==========

@app.post(
    "/api/v1/auth/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Authentication"],
    summary="Регистрация пользователя"
)
async def register_user(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.email] = {
        "email": user.email,
        "password": user.password,
        "full_name": user.full_name,
        "auth_provider": "local"
    }

    return MessageResponse(message=f"User {user.email} registered successfully")


@app.post(
    "/api/v1/auth/login",
    response_model=MessageResponse,
    tags=["Authentication"],
    summary="Вход пользователя"
)
async def login_user(user: UserLogin, response: Response):
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if users_db[user.email].get("password") != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response.set_cookie(
        key="access_token",
        value=f"demo-token-{user.email}",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        path="/"
    )

    return MessageResponse(message="Login successful")


@app.post(
    "/api/v1/auth/logout",
    response_model=MessageResponse,
    tags=["Authentication"],
    summary="Выход пользователя"
)
async def logout_user(response: Response):
    response.delete_cookie("access_token", path="/")
    return MessageResponse(message="Logout successful")


@app.get(
    "/api/v1/auth/me",
    tags=["Authentication"],
    summary="Получить текущего пользователя"
)
async def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not token.startswith("demo-token-"):
        raise HTTPException(status_code=401, detail="Invalid token")

    email = token.replace("demo-token-", "")
    user = users_db.get(email)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "email": user["email"],
        "full_name": user.get("full_name"),
        "auth_provider": user.get("auth_provider", "local")
    }


@app.get(
    "/api/v1/users/",
    tags=["Users"],
    summary="Получить список пользователей"
)
async def get_users():
    result = []

    for user in users_db.values():
        result.append({
            "email": user["email"],
            "full_name": user.get("full_name"),
            "auth_provider": user.get("auth_provider", "local"),
            "yandex_id": user.get("yandex_id")
        })

    return result


# ========== YANDEX OAUTH ==========

@app.get(
    "/api/v1/auth/oauth/yandex",
    tags=["OAuth"],
    summary="Войти через Яндекс"
)
async def yandex_oauth_start():
    if not settings.YANDEX_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="YANDEX_CLIENT_ID is not configured"
        )

    if not settings.YANDEX_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="YANDEX_CLIENT_SECRET is not configured"
        )

    state = secrets.token_urlsafe(32)
    oauth_states.add(state)

    params = {
        "response_type": "code",
        "client_id": settings.YANDEX_CLIENT_ID,
        "redirect_uri": settings.YANDEX_REDIRECT_URI,
        "state": state,
    }

    yandex_url = "https://oauth.yandex.ru/authorize?" + urlencode(params)

    return RedirectResponse(yandex_url)


@app.get(
    "/api/v1/auth/oauth/yandex/callback",
    tags=["OAuth"],
    summary="Callback Яндекс OAuth"
)
async def yandex_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None
):
    if error:
        raise HTTPException(status_code=400, detail=f"Yandex OAuth error: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    if not state or state not in oauth_states:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    oauth_states.remove(state)

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Failed to get token from Yandex",
                    "response": token_response.text
                }
            )

        token_data = token_response.json()
        yandex_access_token = token_data.get("access_token")

        if not yandex_access_token:
            raise HTTPException(status_code=400, detail="Access token not found")

        user_response = await client.get(
            "https://login.yandex.ru/info",
            params={"format": "json"},
            headers={
                "Authorization": f"OAuth {yandex_access_token}"
            }
        )

        if user_response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Failed to get user info from Yandex",
                    "response": user_response.text
                }
            )

        yandex_user = user_response.json()

    email = yandex_user.get("default_email")

    if not email:
        emails = yandex_user.get("emails", [])
        email = emails[0] if emails else None

    if not email:
        login = yandex_user.get("login")
        email = f"{login}@yandex.ru" if login else None

    if not email:
        raise HTTPException(status_code=400, detail="Yandex did not return email")

    full_name = (
        yandex_user.get("real_name")
        or yandex_user.get("display_name")
        or yandex_user.get("login")
        or "Yandex User"
    )

    users_db[email] = {
        "email": email,
        "password": None,
        "full_name": full_name,
        "auth_provider": "yandex",
        "yandex_id": yandex_user.get("id")
    }

    redirect_response = RedirectResponse(url="/api/docs")
    redirect_response.set_cookie(
        key="access_token",
        value=f"demo-token-{email}",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        path="/"
    )

    return redirect_response


# ========== СИСТЕМНЫЕ ЭНДПОИНТЫ ==========

@app.get("/", tags=["System"], summary="Главная страница API")
async def root():
    return {
        "message": "SPA Salon API",
        "environment": settings.ENVIRONMENT,
        "docs": "/api/docs" if settings.ENVIRONMENT != "production" else "disabled",
        "users_count": len(users_db)
    }


@app.get("/health", tags=["System"], summary="Проверка работоспособности сервера")
async def health_check():
    return {"status": "ok"}