from fastapi import Response, status, HTTPException, Depends, APIRouter, Path
from sqlalchemy.orm import Session
from config.database import get_db


# Models and Schemas
from app.vacancies import models, schemas

router = APIRouter(
    tags=["Vacancies"]
)


@router.get(
    path="/vacancies",
    status_code=status.HTTP_200_OK,
    summary="Show all the vacancies",
    response_model=list[schemas.VacancyOut],
)
def read_users(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Returns all vacancies created.
    """
    all_vacaciones = db.query(models.Vacancy).offset(skip).limit(limit).all()

    return all_vacaciones


@router.post(
    path="/vacancies",
    status_code=status.HTTP_201_CREATED,
    summary="Create a vacancy",
    response_model=schemas.VacancyOut
)
def create_user(
        vacancy: schemas.CreateVacancy,
        db: Session = Depends(get_db)
):
    """
    Create a vacancy.
    """

    db_vacancy = models.Vacancy(**vacancy.dict())
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)

    return db_vacancy
