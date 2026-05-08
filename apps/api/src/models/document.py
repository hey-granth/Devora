from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class DocumentBase(SQLModel):
    source_url: str | None = None
    title: str
    content: str
    doc_type: str = Field(default="markdown")  # 'markdown' | 'openapi' | 'changelog'
    metadata: dict[str, Any] = Field(default_factory=dict)


class Document(DocumentBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    org_id: UUID = Field(foreign_key="organizations.id")
    embedding: str | None = None  # Will be stored as VECTOR(1536)
    ingested_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    organization: "Organization" = Relationship(back_populates="documents")
    friction_signals: list["FrictionSignal"] = Relationship(
        back_populates="related_document"
    )


class DocumentCreate(SQLModel):
    source_url: str | None = None
    title: str
    content: str
    doc_type: str = "markdown"
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentUpdate(SQLModel):
    title: str | None = None
    content: str | None = None
    doc_type: str | None = None
    metadata: dict[str, Any] | None = None


class DocumentRead(SQLModel):
    id: UUID
    org_id: UUID
    source_url: str | None
    title: str
    doc_type: str
    ingested_at: datetime
    metadata: dict[str, Any]
