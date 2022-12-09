from fastapi import Response, status, HTTPException, Depends, APIRouter, Path
from sqlalchemy.orm import Session
from config.database import get_db


# Models and Schemas
from app.skills import models, schemas

router = APIRouter(
    tags=["Skills"]
)


@router.get(
    path="/skills",
    status_code=status.HTTP_200_OK,
    summary="Show all skills",
    response_model=list[schemas.SkillOutUserId],
)
def get_all_skills(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Returns all skills created.
    """
    all_skills = db.query(models.Skill).offset(skip).limit(limit).all()

    return all_skills


@router.get(
    path="/users/{user_id}/skills/",
    status_code=status.HTTP_200_OK,
    summary="Show an specific skills from user",
    response_model=list[schemas.SkillOut],
)
def get_user_skills(
        user_id: str,
        db: Session = Depends(get_db)
):
    """
    Returns user skill.
    """
    user_skills = db.query(models.Skill).filter(
        models.Skill.IdUserSkill == user_id).all()

    return user_skills


@router.post(
    path="/users/{user_id}/skills/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SkillOut,
    summary="Create skills for a specific user",
)
def create_skill_for_user(
    user_id: str,
    skill: schemas.CreateSkill,
    db: Session = Depends(get_db)
):
    """
    Creates additional information for the user.
    """
    add_skill = models.Skill(
        **skill.dict(), IdUserSkill=user_id)
    db.add(add_skill)
    db.commit()
    db.refresh(add_skill)

    return add_skill
