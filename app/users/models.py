import uuid
from sqlalchemy import String, Integer, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base


class User(Base):
    __tablename__ = "users"

    UserId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Email = Column(String(50), nullable=False, unique=True)
    YearsPreviousExperience = Column(Integer, nullable=False)

    # Relations
    Skills = relationship(
        "UserSkill", back_populates="YearsOfSkill")
