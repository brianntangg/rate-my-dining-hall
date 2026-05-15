from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class ReviewCreate(BaseModel):
    """Review creation schema"""

    dining_hall_id: int
    rating: int
    text: str

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: int) -> int:
        """Validate rating is between 1 and 5"""
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate review text is at least 10 characters"""
        if len(v.strip()) < 10:
            raise ValueError("Review text must be at least 10 characters")
        return v.strip()


class ReviewResponse(BaseModel):
    """Review response schema"""

    id: int
    user_id: int
    dining_hall_id: int
    rating: int
    text: str
    created_at: datetime
    upvotes: int = 0
    downvotes: int = 0
    score: int = 0

    class Config:
        from_attributes = True


class VoteCreate(BaseModel):
    """Vote creation schema"""

    review_id: int
    value: int

    @field_validator("value")
    @classmethod
    def validate_value(cls, v: int) -> int:
        """Validate vote value is -1 or 1"""
        if v not in [-1, 1]:
            raise ValueError("Vote value must be -1 or 1")
        return v


class VotesResponse(BaseModel):
    """Votes response schema"""

    upvotes: int
    downvotes: int
    score: int
