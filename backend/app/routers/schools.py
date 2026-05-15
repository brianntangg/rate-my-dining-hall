from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, func
from typing import List, Optional
from app.database import get_session
from app.models.school import School
from app.models.dining_hall import DiningHall
from app.models.review import Review
from app.schemas.school import SchoolResponse, DiningHallResponse

router = APIRouter()


@router.get("/schools", response_model=List[SchoolResponse])
async def get_schools(session: Session = Depends(get_session)):
    """Get all schools"""
    schools = session.exec(select(School)).all()
    return schools


@router.get("/dining-halls", response_model=List[DiningHallResponse])
async def get_dining_halls(
    school_id: Optional[int] = Query(None),
    session: Session = Depends(get_session),
):
    """Get dining halls, optionally filtered by school_id"""
    query = select(DiningHall)

    if school_id is not None:
        query = query.where(DiningHall.school_id == school_id)

    dining_halls = session.exec(query).all()

    # Calculate average rating for each dining hall
    response = []
    for hall in dining_halls:
        avg_rating = session.exec(
            select(func.avg(Review.rating)).where(Review.dining_hall_id == hall.id)
        ).first()

        response.append(
            DiningHallResponse(
                id=hall.id,
                name=hall.name,
                school_id=hall.school_id,
                average_rating=float(avg_rating) if avg_rating else None,
            )
        )

    return response


@router.get("/dining-halls/{id}", response_model=DiningHallResponse)
async def get_dining_hall(
    id: int,
    session: Session = Depends(get_session),
):
    """Get a single dining hall by ID"""
    hall = session.get(DiningHall, id)

    if not hall:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dining hall not found",
        )

    # Calculate average rating
    avg_rating = session.exec(
        select(func.avg(Review.rating)).where(Review.dining_hall_id == hall.id)
    ).first()

    return DiningHallResponse(
        id=hall.id,
        name=hall.name,
        school_id=hall.school_id,
        average_rating=float(avg_rating) if avg_rating else None,
    )
