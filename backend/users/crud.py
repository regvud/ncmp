from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext

from backend import models, schemas
from backend.db import db_dependency, save_db_model, update_db_model

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["Users"])


# USER
def get_user_by_email(db: db_dependency, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_user_by_id(db: db_dependency, id: int):
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/create", response_model=schemas.User)
async def user_create(db: db_dependency, user: schemas.UserCreate):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )

    if existing_user:
        raise HTTPException(status_code=404, detail="User already exist")

    hashed_password = pwd_context.hash(user.password)

    user.password = hashed_password

    profile = models.Profile()
    new_user = models.User(**user.model_dump(), profile=profile)

    save_db_model(db, new_user)
    return new_user


@router.get("/", response_model=list[schemas.User])
async def user_list(db: db_dependency):
    return db.query(models.User).all()


@router.get("/{user_id}", response_model=schemas.User)
async def user_by_id(db: db_dependency, user_id: int):
    return get_user_by_id(db, user_id)


# PROFILE
def get_profile(db: db_dependency, user_id: int):
    db_profile = (
        db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    )

    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@router.get("/{user_id}/profile", response_model=schemas.Profile)
async def user_profile(db: db_dependency, user_id: int):
    return get_profile(db, user_id)


@router.put("/{user_id}/profile", response_model=schemas.Profile)
async def profile_update(
    db: db_dependency, user_id: int, updated_profile: schemas.ProfileUpdate
):
    db_profile = get_profile(db, user_id)

    for k, v in updated_profile:
        setattr(db_profile, k, v)

    update_db_model(db, db_profile)
    return db_profile
