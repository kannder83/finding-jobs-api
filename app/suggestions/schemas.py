import uuid as uuid_pkg

from pydantic import BaseModel, Field


class Suggestion(BaseModel):
    VacancyID: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, example="982f79a3-71b9-46f3-9d47-4600e29da720")
    Affinity: float = Field(..., example=100.00)
