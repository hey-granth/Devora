from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class EventBase(SQLModel):
    sdk_name: str | None = None
    sdk_version: str | None = None
    endpoint: str = Field(index=True)
    http_method: str | None = None
    status_code: int = Field(index=True)
    latency_ms: int | None = None
    error_type: str | None = None
    error_message: str | None = None
    runtime: str | None = None
    timestamp: datetime = Field(index=True)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Event(EventBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    developer_id: UUID | None = Field(foreign_key="developers.id")
    org_id: UUID = Field(foreign_key="organizations.id")

    # Relationships
    developer: Optional["Developer"] = Relationship(back_populates="events")
    organization: "Organization" = Relationship(back_populates="events")


class EventCreate(SQLModel):
    developer_id: str  # caller's external identifier
    sdk_name: str | None = None
    sdk_version: str | None = None
    endpoint: str
    http_method: str | None = None
    status_code: int
    latency_ms: int | None = None
    error_type: str | None = None
    error_message: str | None = None
    runtime: str | None = None
    timestamp: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class EventRead(SQLModel):
    id: UUID
    developer_id: UUID | None
    org_id: UUID
    sdk_name: str | None
    sdk_version: str | None
    endpoint: str
    http_method: str | None
    status_code: int
    latency_ms: int | None
    error_type: str | None
    error_message: str | None
    runtime: str | None
    timestamp: datetime
    metadata: dict[str, Any]
