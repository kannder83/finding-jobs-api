import uuid as uuid_pkg

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date


class CreateSkill(BaseModel):
    SkillName: str = Field(..., example="python", max_length=50)
    YearsOfExperience: int = Field(..., example=2)

    class Config:
        orm_mode = True


class SkillOut(CreateSkill):
    SkillId: int = Field(..., example=1)


class SkillOutUserId(SkillOut):
    IdUserSkill: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, example="982f79a3-71b9-46f3-9d47-4600e29da720")


class SkillOutVacancyId(SkillOut):
    IdVancancySkill: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, example="982f79a3-71b9-46f3-9d47-4600e29da720")
