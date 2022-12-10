import uuid as uuid_pkg

from pydantic import BaseModel, EmailStr, Field


# import schemas
from app.skills.schemas import SkillOut


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
