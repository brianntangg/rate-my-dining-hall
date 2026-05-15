"""
Seed script to populate the database with initial data for Vanderbilt University
"""
from sqlmodel import Session, select
from app.database import engine
from app.models.school import School
from app.models.dining_hall import DiningHall


def seed_database():
    """Seed the database with Vanderbilt school and dining halls"""
    with Session(engine) as session:
        # Check if Vanderbilt school already exists
        existing_school = session.exec(
            select(School).where(School.allowed_domain == "vanderbilt.edu")
        ).first()

        if existing_school:
            print("Vanderbilt school already exists. Skipping seed.")
            school = existing_school
        else:
            # Create Vanderbilt school
            school = School(
                name="Vanderbilt University",
                allowed_domain="vanderbilt.edu"
            )
            session.add(school)
            session.commit()
            session.refresh(school)
            print(f"Created school: {school.name}")

        # Define dining halls
        dining_halls = [
            "Commons",
            "E. Bronson Ingram",
            "Rand",
            "2301"
        ]

        # Check existing dining halls
        existing_halls = session.exec(
            select(DiningHall).where(DiningHall.school_id == school.id)
        ).all()
        existing_hall_names = {hall.name for hall in existing_halls}

        # Add missing dining halls
        for hall_name in dining_halls:
            if hall_name not in existing_hall_names:
                hall = DiningHall(
                    name=hall_name,
                    school_id=school.id
                )
                session.add(hall)
                print(f"Created dining hall: {hall_name}")
            else:
                print(f"Dining hall already exists: {hall_name}")

        session.commit()

        print("\nSeed completed successfully!")
        print(f"School: {school.name}")
        print(f"Total dining halls: {len(dining_halls)}")


if __name__ == "__main__":
    print("Starting database seed...")
    seed_database()
