from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    role: str = Field(default="member")  # 'owner' | 'admin' | 'member'


class User(UserBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    org_id: UUID = Field(foreign_key="organizations.id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: datetime | None = None

    # Relationships
    organization: "Organization" = Relationship(back_populates="users")


class UserCreate(SQLModel):
    email: str
    password: str
    role: str = "member"


class UserUpdate(SQLModel):
    email: str | None = None
    role: str | None = None


class UserRead(SQLModel):
    id: UUID
    org_id: UUID
    email: str
    role: str
    created_at: datetime


class UserLogin(SQLModel):
    email: str
    password: str
