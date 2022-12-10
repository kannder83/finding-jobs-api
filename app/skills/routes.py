from fastapi import Response, status, HTTPException, Depends, APIRouter, Path
from sqlalchemy.orm import Session
from config.database import get_db


# Models and Schemas
from app.skills import models, schemas
from app.users.models import User
from app.vacancies.models import Vacancy

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
    try:
        all_skills = db.query(models.UserSkill).offset(skip).limit(limit).all()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if (all_skills is None) or (len(all_skills) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found")

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
    try:
        user_skills = db.query(models.UserSkill).filter(
            models.UserSkill.IdUserSkill == user_id).all()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if (user_skills is None) or (len(user_skills) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"UserID: {user_id} Not Found")

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
    Create skills for a specific user.
    """

    try:
        valid_user_id = db.query(User).filter(
            User.UserId == user_id).first()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if valid_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"UserID: {user_id} not found")

    try:
        add_skill = models.UserSkill(
            **skill.dict(), IdUserSkill=user_id)
        db.add(add_skill)
        db.commit()
        db.refresh(add_skill)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    return add_skill


@router.get(
    path="/required-skills",
    status_code=status.HTTP_200_OK,
    summary="Show all skills",
    response_model=list[schemas.SkillOutVacancyId],
)
def get_all_skills(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Returns all skills created.
    """
    try:
        all_skills = db.query(models.RequiredSkill).offset(
            skip).limit(limit).all()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if (all_skills is None) or (len(all_skills) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found")

    return all_skills


@router.get(
    path="/vacancies/{vacancy_id}/skills/",
    status_code=status.HTTP_200_OK,
    summary="Show an specific skills from vacancy",
    response_model=list[schemas.SkillOut],
)
def get_vacancy_skills(
        vacancy_id: str,
        db: Session = Depends(get_db)
):
    """
    Returns vacancy skill.
    """
    try:
        vacancy_skills = db.query(models.RequiredSkill).filter(
            models.RequiredSkill.IdVancancySkill == vacancy_id).all()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if (vacancy_skills is None) or (len(vacancy_skills) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"VacancyId: {vacancy_id} Not Found")

    return vacancy_skills


@router.post(
    path="/vacancies/{vacancy_id}/skills/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SkillOut,
    summary="Create skills for a specific vacancy",
)
def create_skill_for_vacancy(
    vacancy_id: str,
    skill: schemas.CreateSkill,
    db: Session = Depends(get_db)
):
    """
    Create skills for a specific vacancy.
    """

    try:
        valid_vacancy_id = db.query(Vacancy).filter(
            Vacancy.VacancyId == vacancy_id).first()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if valid_vacancy_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"VacancyId: {vacancy_id} not found")

    try:
        add_skill = models.RequiredSkill(
            **skill.dict(), IdVancancySkill=vacancy_id)
        db.add(add_skill)
        db.commit()
        db.refresh(add_skill)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    return add_skill
