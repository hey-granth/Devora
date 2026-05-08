from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class FrictionSignalBase(SQLModel):
    endpoint: str = Field(index=True)
    error_type: str | None = None
    occurrence_count: int = Field(default=1)
    resolved: bool = Field(default=False, index=True)


class FrictionSignal(FrictionSignalBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    org_id: UUID = Field(foreign_key="organizations.id")
    developer_id: UUID | None = Field(foreign_key="developers.id")
    first_seen_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen_at: datetime = Field(default_factory=datetime.utcnow)
    related_document_id: UUID | None = Field(foreign_key="documents.id")

    # Relationships
    organization: "Organization" = Relationship(back_populates="friction_signals")
    developer: Optional["Developer"] = Relationship(back_populates="friction_signals")
    related_document: Optional["Document"] = Relationship(
        back_populates="friction_signals"
    )


class FrictionSignalCreate(SQLModel):
    endpoint: str
    error_type: str | None = None
    developer_id: UUID | None = None
    related_document_id: UUID | None = None


class FrictionSignalUpdate(SQLModel):
    resolved: bool | None = None
    related_document_id: UUID | None = None


class FrictionSignalRead(SQLModel):
    id: UUID
    org_id: UUID
    developer_id: UUID | None
    endpoint: str
    error_type: str | None
    occurrence_count: int
    first_seen_at: datetime
    last_seen_at: datetime
    resolved: bool
    related_document_id: UUID | None
