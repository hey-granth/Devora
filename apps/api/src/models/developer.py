from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class DeveloperBase(SQLModel):
    external_id: str = Field(index=True)
    email: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Developer(DeveloperBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    org_id: UUID = Field(foreign_key="organizations.id")
    first_seen_at: datetime = Field(default_factory=datetime.utcnow)
    last_active_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    organization: "Organization" = Relationship(back_populates="developers")
    events: list["Event"] = Relationship(back_populates="developer")
    friction_signals: list["FrictionSignal"] = Relationship(back_populates="developer")


class DeveloperCreate(SQLModel):
    external_id: str
    email: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DeveloperUpdate(SQLModel):
    email: str | None = None
    metadata: dict[str, Any] | None = None


class DeveloperRead(SQLModel):
    id: UUID
    org_id: UUID
    external_id: str
    email: str | None
    first_seen_at: datetime
    last_active_at: datetime
    metadata: dict[str, Any]
