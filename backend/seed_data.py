from sqlalchemy.orm import Session

from .models import Student


def seed_students(db: Session):
    existing_student = db.query(Student).first()

    if existing_student:
        return

    students = [
        Student(
            name="Arun Kumar",
            email="arun@example.com",
            age=21,
        ),
        Student(
            name="Priya Sharma",
            email="priya@example.com",
            age=22,
        ),
        Student(
            name="Daniel Lee",
            email="daniel@example.com",
            age=20,
        ),
        Student(
            name="Aisha Rahman",
            email="aisha@example.com",
            age=23,
        ),
    ]

    db.add_all(students)
    db.commit()