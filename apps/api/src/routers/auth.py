from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..redis import get_redis_client
from ..schemas.auth import TokenResponse, UserLogin, UserRegister
from ..services.auth import AuthService

router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_session),
):
    """Register a new organization and owner user."""
    auth_service = AuthService(session)

    # Check if organization already exists
    existing_org = await auth_service.get_org_by_slug(user_data.org_slug)
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "Organization already exists", "code": "ORG_EXISTS"},
        )

    # Create organization and user
    result = await auth_service.register_user(user_data)
    return result


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    """Login user and return tokens."""
    auth_service = AuthService(session)

    result = await auth_service.login_user(user_data.email, user_data.password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid credentials", "code": "INVALID_CREDENTIALS"},
        )

    return result


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    session: AsyncSession = Depends(get_session),
    redis_client=Depends(get_redis_client),
):
    """Refresh access token using refresh token."""
    auth_service = AuthService(session)

    result = await auth_service.refresh_access_token(refresh_token, redis_client)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid refresh token", "code": "INVALID_REFRESH_TOKEN"},
        )

    return result


@router.post("/logout")
async def logout(
    refresh_token: str,
    redis_client=Depends(get_redis_client),
):
    """Logout by revoking refresh token."""
    auth_service = AuthService(session=None)
    await auth_service.revoke_refresh_token(refresh_token, redis_client)

    return {"message": "Logged out successfully"}
