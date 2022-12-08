from fastapi import Response, status, HTTPException, Depends, APIRouter, Path
from sqlalchemy.orm import Session
from config.database import get_db


router = APIRouter(
    tags=["Test"]
)


@router.get(
    path="/test",
    status_code=status.HTTP_200_OK,
    summary="Testing",
    # response_model=schemas.Register
)
def get_all_songs(
    skip: int = 0,
    limit: int = 10,
    # db: Session = Depends(get_db)
):
    return {"working": "Fine!"}
