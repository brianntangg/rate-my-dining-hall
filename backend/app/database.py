from sqlmodel import create_engine, Session, SQLModel
from app.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session


def init_db():
    """Initialize database tables (for development only)"""
    SQLModel.metadata.create_all(engine)
