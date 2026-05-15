from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


class Vote(SQLModel, table=True):
    """Vote model"""

    __tablename__ = "votes"
    __table_args__ = (
        UniqueConstraint("user_id", "review_id", name="unique_user_review_vote"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    review_id: int = Field(foreign_key="reviews.id")
    value: int = Field(ge=-1, le=1)  # -1 (downvote) or 1 (upvote)

    # Relationships
    user: "User" = Relationship(back_populates="votes")
    review: "Review" = Relationship(back_populates="votes")
