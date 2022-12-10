from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from config.database import get_db


# Models and Schemas
from app.users import models, schemas

router = APIRouter(
    tags=["Users"]
)


@router.get(
    path="/users",
    status_code=status.HTTP_200_OK,
    summary="Show all the users",
    response_model=list[schemas.UserOut],
)
def get_all_users(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Returns all users created.
    """
    try:
        all_users = db.query(models.User).offset(skip).limit(limit).all()
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if (all_users is None) or (len(all_users) == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found Users")

    return all_users


@router.get(
    path="/users/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Show an specific user",
    response_model=schemas.UserOut,
)
def get_user_by_id(
        user_id: str,
        db: Session = Depends(get_db)
):
    """
    Returns specific user.
    """
    try:
        user_by_id = db.query(models.User).filter(
            models.User.UserId == user_id).first()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if user_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"UserID: {user_id} Not Found")

    return user_by_id


@router.post(
    path="/users",
    status_code=status.HTTP_201_CREATED,
    summary="Create an user",
    response_model=schemas.UserOut
)
def create_user(
        user: schemas.CreateUser,
        db: Session = Depends(get_db)
):
    """
    Create an user.
    """
    try:
        db_user = db.query(models.User).filter(
            models.User.Email == user.Email).first()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    return db_user


@router.delete(
    path="/users/{user_id}",
    summary="Delete an user by Id",
    status_code=status.HTTP_202_ACCEPTED,
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete an user by ID.
    """
    try:
        user_query = db.query(models.User).filter(
            models.User.UserId == user_id)
        user = user_query.first()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"UserId: {user_id} not found")

    try:
        user_query.delete(synchronize_session=False)
        db.commit()

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"something was wrong. Please try again later.")

    return {"detail": f"UserId: {user_id} was deleted."}
