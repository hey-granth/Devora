
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models import User
from ..utils.auth import hash_password


class UserService:
    """Service for user operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_users(
        self,
        org_id: str,
        limit: int = 50,
        cursor: str | None = None,
    ) -> list[User]:
        """List users in organization with cursor pagination."""
        statement = select(User).where(User.org_id == org_id)

        if cursor:
            statement = statement.where(User.id > cursor)

        statement = statement.order_by(User.id).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create_user(
        self,
        org_id: str,
        email: str,
        password: str,
        role: str = "member",
    ) -> User:
        """Create a new user."""
        hashed_password = hash_password(password)

        user = User(
            org_id=org_id,
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete_user(self, user_id: str, org_id: str) -> bool:
        """Delete a user from organization."""
        statement = select(User).where(
            User.id == user_id,
            User.org_id == org_id,
        )
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()

        return True
