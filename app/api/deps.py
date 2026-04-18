from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.services.auth_service import AuthService

# HTTP Bearer схема для Swagger (опционально, для тестирования через Authorization header)
security = HTTPBearer(auto_error=False)


async def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
) -> User:
    """
    Получение текущего пользователя из JWT токена в HttpOnly cookie.

    Args:
        request: FastAPI Request объект (для доступа к cookies)
        db: Сессия базы данных

    Returns:
        User: Объект текущего пользователя

    Raises:
        HTTPException: 401 если пользователь не авторизован
        HTTPException: 403 если пользователь неактивен
    """
    # Пытаемся получить токен из cookie
    token = request.cookies.get("access_token")

    # Если нет в cookie, пробуем из Authorization header (для тестирования в Swagger)
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")

    # Если токен не найден нигде
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем сервис аутентификации
    auth_service = AuthService(db)

    # Проверяем токен и получаем пользователя
    user = await auth_service.get_user_from_token(token)

    # Если пользователь не найден или токен невалидный
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем, активен ли пользователь
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )

    return user


async def get_current_user_optional(
        request: Request,
        db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Получение текущего пользователя (опционально, не вызывает ошибку).

    Используется для эндпоинтов, которые работают и с авторизацией, и без неё.

    Args:
        request: FastAPI Request объект
        db: Сессия базы данных

    Returns:
        Optional[User]: Объект пользователя или None
    """
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None


async def get_current_user_websocket(
        token: str,
        db: Session
) -> Optional[User]:
    """
    Получение пользователя из токена для WebSocket соединений.

    Args:
        token: JWT токен из WebSocket handshake
        db: Сессия базы данных

    Returns:
        Optional[User]: Объект пользователя или None
    """
    if not token:
        return None

    auth_service = AuthService(db)
    user = await auth_service.get_user_from_token(token)

    return user if user and user.is_active else None