from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, func
from typing import List
from app.database import get_session
from app.models.user import User
from app.models.review import Review
from app.models.vote import Vote
from app.models.dining_hall import DiningHall
from app.schemas.review import ReviewCreate, ReviewResponse
from app.auth import get_current_user

router = APIRouter()


def calculate_review_votes(review: Review, session: Session) -> dict:
    """Calculate vote counts and score for a review"""
    upvotes = session.exec(
        select(func.count(Vote.id)).where(
            Vote.review_id == review.id,
            Vote.value == 1
        )
    ).first() or 0

    downvotes = session.exec(
        select(func.count(Vote.id)).where(
            Vote.review_id == review.id,
            Vote.value == -1
        )
    ).first() or 0

    score = upvotes - downvotes

    return {
        "upvotes": upvotes,
        "downvotes": downvotes,
        "score": score,
    }


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    request: ReviewCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create a new review"""
    # Verify dining hall exists
    dining_hall = session.get(DiningHall, request.dining_hall_id)
    if not dining_hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dining hall not found",
        )

    # Create review
    new_review = Review(
        user_id=current_user.id,
        dining_hall_id=request.dining_hall_id,
        rating=request.rating,
        text=request.text,
    )

    session.add(new_review)
    session.commit()
    session.refresh(new_review)

    # Calculate votes (will be 0 for new review)
    votes_data = calculate_review_votes(new_review, session)

    return ReviewResponse(
        id=new_review.id,
        user_id=new_review.user_id,
        dining_hall_id=new_review.dining_hall_id,
        rating=new_review.rating,
        text=new_review.text,
        created_at=new_review.created_at,
        **votes_data,
    )


@router.get("", response_model=List[ReviewResponse])
async def get_reviews(
    dining_hall_id: int = Query(...),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    """Get reviews for a dining hall, sorted by vote score"""
    # Get reviews
    reviews = session.exec(
        select(Review)
        .where(Review.dining_hall_id == dining_hall_id)
        .offset(offset)
        .limit(limit)
    ).all()

    # Calculate votes for each review and create response
    response = []
    for review in reviews:
        votes_data = calculate_review_votes(review, session)
        response.append(
            ReviewResponse(
                id=review.id,
                user_id=review.user_id,
                dining_hall_id=review.dining_hall_id,
                rating=review.rating,
                text=review.text,
                created_at=review.created_at,
                **votes_data,
            )
        )

    # Sort by score (descending)
    response.sort(key=lambda r: r.score, reverse=True)

    return response


@router.get("/{id}", response_model=ReviewResponse)
async def get_review(
    id: int,
    session: Session = Depends(get_session),
):
    """Get a single review by ID"""
    review = session.get(Review, id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    # Calculate votes
    votes_data = calculate_review_votes(review, session)

    return ReviewResponse(
        id=review.id,
        user_id=review.user_id,
        dining_hall_id=review.dining_hall_id,
        rating=review.rating,
        text=review.text,
        created_at=review.created_at,
        **votes_data,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete a review (author only)"""
    review = session.get(Review, id)

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    # Check if current user is the author
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews",
        )

    session.delete(review)
    session.commit()

    return None
