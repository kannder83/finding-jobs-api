from fastapi import Response, status, HTTPException, Depends, APIRouter, Path
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
def read_users(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Returns all users created.
    """
    all_users = db.query(models.User).offset(skip).limit(limit).all()

    return all_users


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
    db_user = db.query(models.User).filter(
        models.User.Email == user.Email).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
