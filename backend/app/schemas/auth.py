from pydantic import BaseModel, EmailStr, field_validator
from app.config import settings


class RegisterRequest(BaseModel):
    """Registration request schema"""

    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        """Validate that email ends with allowed domain"""
        if not v.endswith(f"@{settings.ALLOWED_EMAIL_DOMAIN}"):
            raise ValueError(f"Email must end with @{settings.ALLOWED_EMAIL_DOMAIN}")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password length"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class LoginRequest(BaseModel):
    """Login request schema"""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response schema"""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema"""

    id: int
    email: str
    school_id: int

    class Config:
        from_attributes = True
