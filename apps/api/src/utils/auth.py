import hashlib
import secrets
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_session
from ..models import User
from ..services.auth import AuthService


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def generate_api_key() -> str:
    """Generate a new API key."""
    return f"dvr_{secrets.token_hex(32)}"


def hash_api_key(api_key: str) -> str:
    """Hash an API key for storage."""
    salt = settings.api_key_hash_salt.encode("utf-8")
    return hashlib.sha256(f"{api_key}{salt}".encode()).hexdigest()


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def create_refresh_token() -> str:
    """Create a refresh token UUID."""
    return secrets.token_urlsafe(32)


async def verify_token(token: str) -> dict | None:
    """Verify a JWT token and return payload."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = await verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token", "code": "INVALID_TOKEN"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token payload", "code": "INVALID_TOKEN"},
        )

    auth_service = AuthService(session)
    user = await auth_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "User not found", "code": "USER_NOT_FOUND"},
        )

    return user
