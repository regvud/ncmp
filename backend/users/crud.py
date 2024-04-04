from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.db import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users")

session_db = get_session()
db_dependency = Annotated[Session, Depends(get_session)]


def get_user(db: db_dependency, email: int):
    db_user = models.User
    db_user = db.query(db_user).filter(db_user.email == email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_all_users(db: db_dependency):
    return db.query(models.User).all()


@router.post("/create", response_model=schemas.User)
async def user_create(db: db_dependency, user: schemas.UserCreate):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )

    if existing_user:
        ""
        raise HTTPException(status_code=404, detail="User already exist")

    hashed_password = pwd_context.hash(user.password)

    user.password = hashed_password

    profile = models.Profile()
    new_user = models.User(**user.model_dump(), profile=profile)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=list[schemas.User])
async def user_list(db: db_dependency):
    users = get_all_users(db)
    return users
