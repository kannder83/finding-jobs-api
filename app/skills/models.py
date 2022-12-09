from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base


class Skill(Base):
    __tablename__ = "skills"

    SkillId = Column(Integer, primary_key=True, nullable=False, index=True)
    SkillName = Column(String(50), nullable=False)
    YearsOfExperience = Column(Integer, nullable=False)

    # Relations
    IdUserSkill = Column(
        UUID(as_uuid=True), ForeignKey("users.UserId", ondelete="CASCADE"))
    YearsOfSkill = relationship("User", back_populates="Skills")
