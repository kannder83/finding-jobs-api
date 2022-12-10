import uuid
from sqlalchemy import String, Integer, Column, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    VacancyId = Column(UUID(as_uuid=True),
                       primary_key=True, default=uuid.uuid4)
    PositionName = Column(String(50), nullable=False)
    CompanyName = Column(String(50), nullable=False)
    Salary = Column(Integer, nullable=False)
    Currency = Column(String(3), nullable=False)
    VacancyLink = Column(String(200), nullable=False)

    # Relations
    RequiredSkills = relationship(
        "RequiredSkill", back_populates="YearsOfSkill")
