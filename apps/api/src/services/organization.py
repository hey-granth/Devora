
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models import Organization
from ..schemas.organization import OrganizationUpdate


class OrganizationService:
    """Service for organization operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_org_by_id(self, org_id: str) -> Organization | None:
        """Get organization by ID."""
        statement = select(Organization).where(Organization.id == org_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_org_by_slug(self, slug: str) -> Organization | None:
        """Get organization by slug."""
        statement = select(Organization).where(Organization.slug == slug)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def update_org(
        self, org_id: str, org_data: OrganizationUpdate
    ) -> Organization | None:
        """Update organization details."""
        statement = select(Organization).where(Organization.id == org_id)
        result = await self.session.execute(statement)
        org = result.scalar_one_or_none()

        if not org:
            return None

        # Update fields
        if org_data.name is not None:
            org.name = org_data.name
        if org_data.slug is not None:
            org.slug = org_data.slug

        await self.session.commit()
        await self.session.refresh(org)

        return org

    async def update_api_key(
        self, org_id: str, hashed_api_key: str
    ) -> Organization | None:
        """Update organization API key."""
        statement = select(Organization).where(Organization.id == org_id)
        result = await self.session.execute(statement)
        org = result.scalar_one_or_none()

        if not org:
            return None

        org.api_key = hashed_api_key
        await self.session.commit()
        await self.session.refresh(org)

        return org
