
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Request schema for user creation."""

    email: EmailStr
    password: str
    role: str = "member"  # 'owner' | 'admin' | 'member'


class UserResponse(BaseModel):
    """Response schema for user operations."""

    message: str
