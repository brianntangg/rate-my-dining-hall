from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from app.database import get_session
from app.models.user import User
from app.models.review import Review
from app.models.vote import Vote
from app.schemas.review import VoteCreate, VotesResponse
from app.auth import get_current_user

router = APIRouter()


@router.post("", response_model=VotesResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_vote(
    request: VoteCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Create or update a vote (upsert)"""
    # Verify review exists
    review = session.get(Review, request.review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    # Check if user is voting on their own review
    if review.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot vote on your own review",
        )

    # Check if vote already exists
    existing_vote = session.exec(
        select(Vote).where(
            Vote.user_id == current_user.id,
            Vote.review_id == request.review_id,
        )
    ).first()

    if existing_vote:
        # Update existing vote
        existing_vote.value = request.value
        session.add(existing_vote)
    else:
        # Create new vote
        new_vote = Vote(
            user_id=current_user.id,
            review_id=request.review_id,
            value=request.value,
        )
        session.add(new_vote)

    session.commit()

    # Calculate and return vote counts
    upvotes = session.exec(
        select(func.count(Vote.id)).where(
            Vote.review_id == request.review_id,
            Vote.value == 1
        )
    ).first() or 0

    downvotes = session.exec(
        select(func.count(Vote.id)).where(
            Vote.review_id == request.review_id,
            Vote.value == -1
        )
    ).first() or 0

    score = upvotes - downvotes

    return VotesResponse(
        upvotes=upvotes,
        downvotes=downvotes,
        score=score,
    )


@router.get("/{review_id}/votes", response_model=VotesResponse)
async def get_review_votes(
    review_id: int,
    session: Session = Depends(get_session),
):
    """Get vote counts for a review"""
    # Verify review exists
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    # Calculate vote counts
    upvotes = session.exec(
        select(func.count(Vote.id)).where(
            Vote.review_id == review_id,
            Vote.value == 1
        )
    ).first() or 0

    downvotes = session.exec(
        select(func.count(Vote.id)).where(
            Vote.review_id == review_id,
            Vote.value == -1
        )
    ).first() or 0

    score = upvotes - downvotes

    return VotesResponse(
        upvotes=upvotes,
        downvotes=downvotes,
        score=score,
    )
