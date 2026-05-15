from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class DiningHall(SQLModel, table=True):
    """Dining hall model"""

    __tablename__ = "dining_halls"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    school_id: int = Field(foreign_key="schools.id")

    # Relationships
    school: "School" = Relationship(back_populates="dining_halls")
    reviews: List["Review"] = Relationship(back_populates="dining_hall")
