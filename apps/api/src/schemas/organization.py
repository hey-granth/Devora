
from pydantic import BaseModel


class OrganizationUpdate(BaseModel):
    """Request schema for organization update."""

    name: str | None = None
    slug: str | None = None


class ApiKeyResponse(BaseModel):
    """Response schema for API key rotation."""

    api_key: str
