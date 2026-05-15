import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session
from app.models import School, DiningHall, User, Review, Vote


@pytest.fixture(name="session")
def session_fixture():
    """Create a new database session for each test"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Create test school
        school = School(
            name="Vanderbilt University",
            allowed_domain="vanderbilt.edu"
        )
        session.add(school)
        session.commit()
        session.refresh(school)

        # Create test dining hall
        hall = DiningHall(
            name="Test Commons",
            school_id=school.id
        )
        session.add(hall)
        session.commit()

        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with the test database session"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
