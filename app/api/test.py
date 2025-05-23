from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session


# from app.crud import test as crud_test
from app.database import get_db

router = APIRouter()

@router.get("/")
def root(db: Session = Depends(get_db)):
    res = crud_test.get_test(db=db)
    return res