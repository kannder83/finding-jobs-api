from fastapi import Response, status, HTTPException, Depends, APIRouter, Path
from sqlalchemy.orm import Session
from config.database import get_db


# Models and Schemas
from app.skills.models import UserSkill, RequiredSkill
from app.users.models import User
from app.vacancies.models import Vacancy

router = APIRouter(
    tags=["Suggestions"]
)


@router.get(
    path="/suggestions/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Show all the subbestions by user",
    # response_model=list[schemas.UserOut],
)
def get_all_users(
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Returns suggestions by user.
    """
    user_skill: dict = {}
    all_suggestions: list = []

    try:
        # Search user by ID
        user_by_id = db.query(User).filter(User.UserId == user_id).first()

        if user_by_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"UserID: {user_id} Not Found")

        # Get all skill if user exists
        user_skills_by_id = db.query(UserSkill).filter(
            UserSkill.IdUserSkill == user_id).all()

        if (user_skills_by_id is None) or (len(user_skills_by_id) == 0):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"UserID: {user_id} Not Found")

        for skill in user_skills_by_id:
            user_skill.update({skill.SkillName: skill.YearsOfExperience})

        # Get all vacancies
        require_vacancy_skills = db.query(
            RequiredSkill).offset(skip).limit(limit).all()

        if (require_vacancy_skills is None) or (len(require_vacancy_skills) == 0):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Vacancies Not Found")

        for required_skill in require_vacancy_skills:
            if required_skill.SkillName in user_skill:
                skill_name = required_skill.SkillName

                if required_skill.YearsOfExperience <= user_skill.get(skill_name):

                    if required_skill.IdVancancySkill not in all_suggestions:
                        all_suggestions.append(required_skill.IdVancancySkill)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later. {error}")

    if (all_suggestions is None) or (len(all_suggestions) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Suggestion Not Found")

    return all_suggestions
