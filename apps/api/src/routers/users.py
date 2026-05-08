
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models import User
from ..schemas.user import UserCreate, UserRead
from ..services.user import UserService
from ..utils.auth import get_current_user

router = APIRouter()


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin or owner role."""
    if current_user.role not in ("owner", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Insufficient permissions", "code": "FORBIDDEN"},
        )
    return current_user


async def require_owner(current_user: User = Depends(get_current_user)) -> User:
    """Require owner role."""
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Owner access required", "code": "OWNER_REQUIRED"},
        )
    return current_user


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user information."""
    return current_user


@router.get("/", response_model=list[UserRead])
async def list_organization_users(
    current_user: User = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=50, le=500),
    cursor: str | None = Query(default=None),
):
    """List all users in the organization (admin+)."""
    user_service = UserService(session)
    users = await user_service.list_users(
        org_id=current_user.org_id,
        limit=limit,
        cursor=cursor,
    )
    return users


@router.post("/invite", response_model=UserRead)
async def invite_user(
    user_data: UserCreate,
    current_user: User = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
):
    """Invite a new user to the organization (admin+)."""
    user_service = UserService(session)

    # Check if user already exists
    existing_user = await user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "User already exists", "code": "USER_EXISTS"},
        )

    user = await user_service.create_user(
        org_id=current_user.org_id,
        email=user_data.email,
        password=user_data.password,
        role=user_data.role,
    )

    return user


@router.delete("/{user_id}")
async def remove_user(
    user_id: str,
    current_user: User = Depends(require_owner),
    session: AsyncSession = Depends(get_session),
):
    """Remove a user from the organization (owner only)."""
    user_service = UserService(session)

    # Cannot remove yourself
    if user_id == str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Cannot remove yourself", "code": "CANNOT_REMOVE_SELF"},
        )

    success = await user_service.delete_user(user_id, current_user.org_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "User not found", "code": "USER_NOT_FOUND"},
        )

    return {"message": "User removed successfully"}
