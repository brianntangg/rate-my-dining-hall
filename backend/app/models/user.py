from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    """User model"""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    school_id: int = Field(foreign_key="schools.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    school: "School" = Relationship(back_populates="users")
    reviews: List["Review"] = Relationship(back_populates="user")
    votes: List["Vote"] = Relationship(back_populates="user")
