from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class OrganizationBase(SQLModel):
    name: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    api_key: str = Field(unique=True)
    plan: str = Field(default="free")


class Organization(OrganizationBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: datetime | None = None

    # Relationships
    users: list["User"] = Relationship(back_populates="organization")
    developers: list["Developer"] = Relationship(back_populates="organization")
    events: list["Event"] = Relationship(back_populates="organization")
    documents: list["Document"] = Relationship(back_populates="documents")
    friction_signals: list["FrictionSignal"] = Relationship(
        back_populates="organization"
    )


class OrganizationCreate(SQLModel):
    name: str
    slug: str


class OrganizationUpdate(SQLModel):
    name: str | None = None
    slug: str | None = None


class OrganizationRead(SQLModel):
    id: UUID
    name: str
    slug: str
    plan: str
    created_at: datetime
