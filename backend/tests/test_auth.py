import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


def test_register_success(client: TestClient):
    """Test successful user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@vanderbilt.edu",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_invalid_email_domain(client: TestClient):
    """Test registration with invalid email domain"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@gmail.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 422  # Validation error


def test_register_short_password(client: TestClient):
    """Test registration with short password"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@vanderbilt.edu",
            "password": "short"
        }
    )
    assert response.status_code == 422  # Validation error


def test_register_duplicate_email(client: TestClient):
    """Test registration with duplicate email"""
    # First registration
    client.post(
        "/api/auth/register",
        json={
            "email": "test@vanderbilt.edu",
            "password": "testpassword123"
        }
    )

    # Try to register again with same email
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@vanderbilt.edu",
            "password": "anotherpassword123"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client: TestClient):
    """Test successful login"""
    # Register user first
    client.post(
        "/api/auth/register",
        json={
            "email": "test@vanderbilt.edu",
            "password": "testpassword123"
        }
    )

    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@vanderbilt.edu",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    """Test login with wrong password"""
    # Register user first
    client.post(
        "/api/auth/register",
        json={
            "email": "test@vanderbilt.edu",
            "password": "testpassword123"
        }
    )

    # Try to login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@vanderbilt.edu",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient):
    """Test login with nonexistent user"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@vanderbilt.edu",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 401


def test_get_me_authenticated(client: TestClient):
    """Test getting current user when authenticated"""
    # Register user
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "test@vanderbilt.edu",
            "password": "testpassword123"
        }
    )
    token = register_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@vanderbilt.edu"
    assert "id" in data
    assert "school_id" in data


def test_get_me_unauthenticated(client: TestClient):
    """Test getting current user when not authenticated"""
    response = client.get("/api/auth/me")
    assert response.status_code == 403  # No credentials provided


def test_get_me_invalid_token(client: TestClient):
    """Test getting current user with invalid token"""
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
