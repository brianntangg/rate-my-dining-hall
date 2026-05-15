from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, schools, reviews, votes

app = FastAPI(title="Rate My Dining Hall API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(schools.router, prefix="/api", tags=["schools"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(votes.router, prefix="/api/votes", tags=["votes"])


@app.get("/ping")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}
