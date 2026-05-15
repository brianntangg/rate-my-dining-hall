from typing import Optional
import os


class Settings:
    """Application settings"""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://rmdh_user:rmdh_password@localhost:5432/rmdh"
    )

    JWT_SECRET: str = os.environ["JWT_SECRET"]
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_DAYS: int = 7

    ALLOWED_EMAIL_DOMAIN: str = os.getenv("ALLOWED_EMAIL_DOMAIN", "vanderbilt.edu")

    # CORS settings — comma-separated list of allowed origins
    BACKEND_CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:5173,http://localhost:3000",
        ).split(",")
    ]


settings = Settings()
