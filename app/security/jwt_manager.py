from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


class JWTManager:
    """Reservado para usos futuros; el flujo activo usa jwt_handler + misma configuración."""

    @staticmethod
    def create_token(data: dict) -> str:
        to_encode = data.copy()
        to_encode["exp"] = datetime.now(timezone.utc) + timedelta(hours=8)
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
