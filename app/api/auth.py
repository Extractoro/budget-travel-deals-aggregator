from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import AuthUserCredentials, UserSchema, TokenResponse
from app.service.auth import user_registration, authenticate_user

router = APIRouter()


@router.post('/signup', description="User registration", response_model=UserSchema)
def signup(credentials: AuthUserCredentials, db: Session = Depends(get_db)):
    user = user_registration(db, credentials)

    if isinstance(user, Exception):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(user))

    return user


@router.post('/login', description="User login", response_model=TokenResponse)
def login(credentials: AuthUserCredentials, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials)
    return user
