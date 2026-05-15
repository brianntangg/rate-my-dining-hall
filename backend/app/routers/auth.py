from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.models.school import School
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_session),
):
    """Register a new user"""
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Get the school for this email domain
    domain = request.email.split("@")[1]
    school = session.exec(
        select(School).where(School.allowed_domain == domain)
    ).first()

    if not school:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No school found for domain {domain}",
        )

    # Create new user
    hashed_password = hash_password(request.password)
    new_user = User(
        email=request.email,
        hashed_password=hashed_password,
        school_id=school.id,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Create access token
    access_token = create_access_token(data={"sub": str(new_user.id)})

    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    session: Session = Depends(get_session),
):
    """Login a user"""
    # Find user
    user = session.exec(
        select(User).where(User.email == request.email)
    ).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user"""
    return current_user
