from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentBase(BaseModel):
    name: str
    email: str
    age: int = Field(gt=0)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Invalid email address")
        return value


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    age: int = Field(gt=0)


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    course_name: str
    credits: int = Field(ge=1, le=6)
    student_id: int


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    course_name: str | None = None
    credits: int | None = Field(default=None, ge=1, le=6)
    student_id: int | None = None


class CourseResponse(CourseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class StudyAdviceRequest(BaseModel):
    prompt: str