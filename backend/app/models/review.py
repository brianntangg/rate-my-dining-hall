from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class Review(SQLModel, table=True):
    """Review model"""

    __tablename__ = "reviews"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    dining_hall_id: int = Field(foreign_key="dining_halls.id")
    rating: int = Field(ge=1, le=5)  # 1-5 stars
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: "User" = Relationship(back_populates="reviews")
    dining_hall: "DiningHall" = Relationship(back_populates="reviews")
    votes: List["Vote"] = Relationship(back_populates="review")
