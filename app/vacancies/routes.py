from fastapi import status, HTTPException, Depends, APIRouter
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
def get_all_vacancies(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Returns all vacancies created.
    """
    try:
        all_vacaciones = db.query(models.Vacancy).offset(
            skip).limit(limit).all()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if (all_vacaciones is None) or (len(all_vacaciones) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found Vacancies")

    return all_vacaciones


@router.get(
    path="/vacancies/{vacancy_id}/",
    status_code=status.HTTP_200_OK,
    summary="Show an specific vacancy",
    response_model=schemas.VacancyOut,
)
def get_vacancy_by_id(
        vacancy_id: str,
        db: Session = Depends(get_db)
):
    """
    Returns specific vacancy.
    """
    try:
        vacancy_by_id = db.query(models.Vacancy).filter(
            models.Vacancy.VacancyId == vacancy_id).first()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if vacancy_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"VacancyId: {vacancy_id} Not Found")

    return vacancy_by_id


@router.post(
    path="/vacancies",
    status_code=status.HTTP_201_CREATED,
    summary="Create a vacancy",
    response_model=schemas.VacancyOut
)
def create_vacancy(
        vacancy: schemas.CreateVacancy,
        db: Session = Depends(get_db)
):
    """
    Create a vacancy.
    """

    try:
        db_vacancy = models.Vacancy(**vacancy.dict())
        db.add(db_vacancy)
        db.commit()
        db.refresh(db_vacancy)

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    return db_vacancy


@router.delete(
    path="/vacancies/{vacancy_id}",
    summary="Delete a vacancy by Id",
    status_code=status.HTTP_202_ACCEPTED,
)
def delete_vacancy(
    vacancy_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a vacancy by ID.
    """
    try:
        vacancy_query = db.query(models.Vacancy).filter(
            models.Vacancy.VacancyId == vacancy_id)
        vacancy = vacancy_query.first()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"VacancyID: {vacancy_id} not found")

    try:
        vacancy_query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    return {"detail": f"VacancyId: {vacancy_id} was deleted."}
