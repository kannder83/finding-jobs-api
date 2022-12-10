from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from config.database import get_db


# Models and Schemas
from app.skills.models import UserSkill, RequiredSkill
from app.users.models import User
from app.suggestions import schemas

router = APIRouter(
    tags=["Suggestions"]
)


@router.get(
    path="/suggestions/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Show all the subbestions by user",
    response_model=list[schemas.Suggestion],
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
    all_vacancies: list = []
    resume_suggestions: list = []

    try:
        # Search user by ID
        user_by_id = db.query(User).filter(User.UserId == user_id).first()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if user_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"UserID: {user_id} Not Found")

    # Get all skill if user exists
    user_skills_by_id = db.query(UserSkill).filter(
        UserSkill.IdUserSkill == user_id).all()

    if (user_skills_by_id is None) or (len(user_skills_by_id) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"UserID: {user_id} Not Found Skills")

    for skill in user_skills_by_id:
        user_skill.update({skill.SkillName: skill.YearsOfExperience})

    # Get all vacancies
    try:
        require_vacancy_skills = db.query(
            RequiredSkill).offset(skip).limit(limit).all()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if (require_vacancy_skills is None) or (len(require_vacancy_skills) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Vacancies Not Found")

    for required_skill in require_vacancy_skills:

        if required_skill.SkillName in user_skill:

            skill_name = required_skill.SkillName
            vacancy_id = required_skill.IdVancancySkill

            if required_skill.YearsOfExperience <= user_skill.get(skill_name):

                if required_skill.IdVancancySkill not in all_suggestions:
                    all_suggestions.append(vacancy_id)

        all_vacancies.append(required_skill.IdVancancySkill)

    if (all_suggestions is None) or (len(all_suggestions) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Suggestion Not Found")

    # Counting repeat ID:
    count_all_vacancies_id = dict(zip(all_vacancies, map(
        lambda x: all_vacancies.count(x), all_vacancies)))

    count_all_suggestion = dict(zip(all_suggestions, map(
        lambda x: all_suggestions.count(x), all_suggestions)))

    # Analisys:
    for item in count_all_vacancies_id.keys():
        if item in count_all_suggestion.keys():
            affinity = count_all_suggestion.get(
                item)/count_all_vacancies_id.get(item)*100

            if affinity >= 50:
                resume_dict_suggestion_vacancies = {
                    "VacancyID": item,
                    "Affinity": round(affinity, 2)
                }
                resume_suggestions.append(resume_dict_suggestion_vacancies)

    return resume_suggestions
