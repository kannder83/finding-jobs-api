import uuid as uuid_pkg

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date


class SkillOut(BaseModel):
    SkillId: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, example="447773f2-7bc8-4565-8fe9-56bf5f31308d")
    SkillName: str = Field(..., example="personal", max_length=50)
    YearsOfExperience: int = Field(..., example=2)

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    FirstName: str = Field(..., example="Juan", max_length=50)
    LastName: str = Field(..., example="Perez", max_length=50)
    Email: EmailStr = Field(..., example="example@xyz.com")
    YearsPreviousExperience: int = Field(..., example=2)

    class Config:
        orm_mode = True


class UserOut(CreateUser):
    UserId: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, example="982f79a3-71b9-46f3-9d47-4600e29da720")

    Skills: list[SkillOut] = []
