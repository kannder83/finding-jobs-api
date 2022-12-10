import uuid as uuid_pkg

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date


# import schemas
from app.skills.schemas import SkillOut


class CreateVacancy(BaseModel):
    PositionName: str = Field(..., example="Developer", max_length=50)
    CompanyName: str = Field(..., example="Stark Industies", max_length=50)
    Salary: int = Field(..., example=2000)
    Currency: str = Field(..., example="USD", max_length=3)
    VacancyLink: str = Field(..., example="www.linkjobs.com", max_length=200)

    class Config:
        orm_mode = True


class VacancyOut(CreateVacancy):
    VacancyId: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, example="982f79a3-71b9-46f3-9d47-4600e29da720")

    RequiredSkills: list[SkillOut] = []
