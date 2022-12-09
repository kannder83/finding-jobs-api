import uuid
from sqlalchemy import String, Integer, Column, ForeignKey
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
        "Skill", back_populates="YearsOfSkill")


"""
Example:
{
 "UserId": uuidv4(),
 "FirstName": "Test Name",
 "LastName": "Test Last Name",
 "Email": "un.test.no.hace.mal@gmail.com",
 "YearsPreviousExperience": 5,
 "Skills": [
   {
     "Python": 1
   },
   {
     "NoSQL": 2
   }
 ]
}

"""
