from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models
from .schemas import StudentCreate, CourseCreate, CourseUpdate


# --------------------
# Student CRUD
# --------------------

def create_student(db: Session, student: StudentCreate):
    existing_student = (
        db.query(models.Student)
        .filter(models.Student.email == student.email)
        .first()
    )

    if existing_student is not None:
        return None

    db_student = models.Student(
        name=student.name,
        email=student.email,
        age=student.age,
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


def get_students(db: Session, min_age: int | None = None):
    query = db.query(models.Student)

    if min_age is not None:
        query = query.filter(models.Student.age >= min_age)

    return query.all()


def get_student(db: Session, student_id: int):
    return (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )


def update_student_age(db: Session, student_id: int, age: int):
    student = get_student(db, student_id)

    if student is None:
        return None

    student.age = age

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return student

def get_student_course_count(db: Session, student_id: int):
    student = get_student(db, student_id)

    if student is None:
        return None

    count = (
        db.query(func.count(models.Course.id))
        .filter(models.Course.student_id == student_id)
        .scalar()
    )

    return count


# --------------------
# Course CRUD
# --------------------

def create_course(db: Session, course: CourseCreate):
    db_course = models.Course(
        course_name=course.course_name,
        credits=course.credits,
        student_id=course.student_id,
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


def get_courses(db: Session):
    return db.query(models.Course).all()


def get_course(db: Session, course_id: int):
    return (
        db.query(models.Course)
        .filter(models.Course.id == course_id)
        .first()
    )


def update_course(
    db: Session,
    course_id: int,
    course_data: CourseUpdate,
):
    course = get_course(db, course_id)

    if course is None:
        return None

    update_data = course_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)

    return course


def delete_course(db: Session, course_id: int):
    course = get_course(db, course_id)

    if course is None:
        return None

    db.delete(course)
    db.commit()

    return course