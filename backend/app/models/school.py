from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class School(SQLModel, table=True):
    """School model"""

    __tablename__ = "schools"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    allowed_domain: str = Field(index=True)

    # Relationships
    dining_halls: List["DiningHall"] = Relationship(back_populates="school")
    users: List["User"] = Relationship(back_populates="school")
