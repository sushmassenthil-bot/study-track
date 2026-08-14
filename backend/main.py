from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .ai import generate_study_advice

from . import crud
from .database import Base, SessionLocal, engine, get_db
from .schemas import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
    CourseCreate,
    CourseResponse,
    CourseUpdate,
    StudyAdviceRequest,
)
from .seed_data import seed_students
from .algorithms import (
    insertion_sort_by_field,
    binary_search_by_name,
    format_roster_report,
    count_students_meeting_min_age,
)


# --------------------
# Database setup
# --------------------

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    seed_students(db)


# --------------------
# FastAPI app
# --------------------

app = FastAPI(title="StudyTrack")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------
# Student endpoints
# --------------------

@app.post(
    "/students/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
):
    return crud.create_student(db, student)


@app.get(
    "/students/",
    response_model=list[StudentResponse],
)
def read_students(
    min_age: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_students(db, min_age)


# IMPORTANT:
# Specific routes must come before /students/{student_id}

@app.get("/students/report")
def get_student_report(
    min_age: int = 21,
    db: Session = Depends(get_db),
):
    students = crud.get_students(db)

    student_dicts = [
        {
            "name": student.name,
            "email": student.email,
            "age": student.age,
        }
        for student in students
    ]

    insertion_sort_by_field(student_dicts, "age")

    report = format_roster_report(student_dicts)

    count = count_students_meeting_min_age(
        student_dicts,
        min_age,
    )

    return {
        "report": report,
        "count_meeting_min_age": count,
    }


@app.get("/students/{student_id}/course-count")
def read_student_course_count(
    student_id: int,
    db: Session = Depends(get_db),
):
    count = crud.get_student_course_count(db, student_id)

    if count is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return {
        "student_id": student_id,
        "course_count": count,
    }


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


@app.patch(
    "/students/{student_id}",
    response_model=StudentResponse,
)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db),
):
    updated_student = crud.update_student_age(
        db,
        student_id,
        student.age,
    )

    if updated_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return updated_student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = crud.delete_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )


# --------------------
# Course endpoints
# --------------------

@app.post(
    "/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
):
    return crud.create_course(db, course)


@app.get(
    "/courses/",
    response_model=list[CourseResponse],
)
def read_courses(
    db: Session = Depends(get_db),
):
    return crud.get_courses(db)


@app.get(
    "/courses/{course_id}",
    response_model=CourseResponse,
)
def read_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = crud.get_course(db, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return course


@app.patch(
    "/courses/{course_id}",
    response_model=CourseResponse,
)
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
):
    updated_course = crud.update_course(
        db,
        course_id,
        course,
    )

    if updated_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return updated_course


@app.delete(
    "/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = crud.delete_course(db, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )


# --------------------
# Algorithm endpoints
# --------------------

@app.get("/algorithms/roster")
def get_roster(
    db: Session = Depends(get_db),
):
    students = crud.get_students(db)

    student_dicts = [
        {
            "name": student.name,
            "email": student.email,
            "age": student.age,
        }
        for student in students
    ]

    insertion_sort_by_field(student_dicts, "age")

    return student_dicts


@app.get("/algorithms/search")
def search_student(
    name: str,
    db: Session = Depends(get_db),
):
    students = crud.get_students(db)

    student_dicts = [
        {
            "name": student.name,
            "email": student.email,
            "age": student.age,
        }
        for student in students
    ]

    # Binary search requires the list to be sorted by name.
    name_sorted_students = sorted(
        student_dicts,
        key=lambda student: student["name"],
    )

    result = binary_search_by_name(
        name_sorted_students,
        name,
    )

    if result == -1:
        raise HTTPException(
            status_code=404,
            detail=f"Student '{name}' not found",
        )

    index = name_sorted_students.index(result)

    return {
        "index": index,
        "student": result,
    }

@app.post("/ai/study-advice")
def study_advice(request: StudyAdviceRequest):
    try:
        advice = generate_study_advice(request.prompt)

        return {
            "advice": advice
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="AI service is currently unavailable.",
        )