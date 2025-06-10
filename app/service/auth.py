from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.models import User
from app.schemas.schemas import AuthUserCredentials
from app.utils.create_access_token import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def user_registration(db: Session, credentials: AuthUserCredentials):
    existing_user = db.query(User).filter(User.username == credentials.username).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = pwd_context.hash(credentials.password)

    new_user = User(username=credentials.username, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, credentials: AuthUserCredentials):
    existing_user = db.query(User).filter(User.username == credentials.username).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not pwd_context.verify(credentials.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    access_token = create_access_token(data={"sub": existing_user.username})

    return {"access_token": access_token, "token_type": "Bearer"}
