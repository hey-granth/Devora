from datetime import timedelta

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models import Organization, User
from ..schemas.auth import TokenResponse, UserRegister
from ..utils.auth import (
    create_access_token,
    create_refresh_token,
    generate_api_key,
    hash_api_key,
    hash_password,
    verify_password,
)


class AuthService:
    """Service for authentication operations."""

    def __init__(self, session: AsyncSession | None):
        self.session = session

    async def get_org_by_slug(self, slug: str) -> Organization | None:
        """Get organization by slug."""
        if not self.session:
            return None
        statement = select(Organization).where(Organization.slug == slug)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        if not self.session:
            return None
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        if not self.session:
            return None
        statement = select(User).where(User.id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def register_user(self, user_data: UserRegister) -> TokenResponse:
        """Register a new organization and owner user."""
        # Create organization
        api_key = generate_api_key()
        hashed_api_key = hash_api_key(api_key)

        org = Organization(
            name=user_data.org_name,
            slug=user_data.org_slug,
            api_key=hashed_api_key,
            plan="free",
        )
        self.session.add(org)
        await self.session.flush()  # Get org.id

        # Create owner user
        hashed_password = hash_password(user_data.password)
        user = User(
            org_id=org.id,
            email=user_data.email,
            hashed_password=hashed_password,
            role="owner",
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        # Generate tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "org_id": str(org.id)}
        )
        refresh_token = create_refresh_token()

        # Store refresh token in Redis (7 days TTL)
        await self._store_refresh_token(refresh_token, str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900,  # 15 minutes
        )

    async def login_user(self, email: str, password: str) -> TokenResponse | None:
        """Login user and return tokens."""
        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None

        # Generate tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "org_id": str(user.org_id)}
        )
        refresh_token = create_refresh_token()

        # Store refresh token in Redis (7 days TTL)
        await self._store_refresh_token(refresh_token, str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900,  # 15 minutes
        )

    async def refresh_access_token(
        self, refresh_token: str, redis_client: redis.Redis
    ) -> TokenResponse | None:
        """Refresh access token using refresh token."""
        # Get user ID from Redis
        user_id = await redis_client.get(f"refresh:{refresh_token}")
        if not user_id:
            return None

        user = await self.get_user_by_id(user_id.decode())
        if not user:
            return None

        # Generate new tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "org_id": str(user.org_id)}
        )
        new_refresh_token = create_refresh_token()

        # Store new refresh token and revoke old one
        await self._store_refresh_token(new_refresh_token, str(user.id))
        await redis_client.delete(f"refresh:{refresh_token}")

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=900,  # 15 minutes
        )

    async def revoke_refresh_token(
        self, refresh_token: str, redis_client: redis.Redis
    ) -> None:
        """Revoke refresh token."""
        await redis_client.delete(f"refresh:{refresh_token}")

    async def _store_refresh_token(self, refresh_token: str, user_id: str) -> None:
        """Store refresh token in Redis with 7 days TTL."""
        import redis.asyncio as redis

        from ..config import settings

        redis_client = redis.from_url(settings.redis_url)
        await redis_client.setex(f"refresh:{refresh_token}", timedelta(days=7), user_id)
