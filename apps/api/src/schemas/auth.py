
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """Request schema for user registration."""

    org_name: str
    org_slug: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Request schema for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response schema for authentication tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until access token expires


class RefreshRequest(BaseModel):
    """Request schema for token refresh."""

    refresh_token: str


class LogoutRequest(BaseModel):
    """Request schema for logout."""

    refresh_token: str
