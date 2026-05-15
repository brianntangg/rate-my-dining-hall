from pydantic import BaseModel
from typing import Optional


class SchoolResponse(BaseModel):
    """School response schema"""

    id: int
    name: str
    allowed_domain: str

    class Config:
        from_attributes = True


class DiningHallResponse(BaseModel):
    """Dining hall response schema"""

    id: int
    name: str
    school_id: int
    average_rating: Optional[float] = None

    class Config:
        from_attributes = True
