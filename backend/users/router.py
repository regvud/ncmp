from fastapi import APIRouter, Depends

import models
import schemas
from auth import authenticated_permission
from db import db_dependency, update_db_model

from .crud import get_profile, get_user_by_id, user_create

router = APIRouter(prefix="/users", tags=["Users"])


# USER
@router.post("/create", response_model=schemas.User)
async def new_user_create(db: db_dependency, user: schemas.UserCreate):
    return user_create(db, user)


@router.get("/", response_model=list[schemas.User])
async def user_list(
    db: db_dependency,
    current_user: schemas.AuthenticatedUser = Depends(authenticated_permission),
):
    print(current_user)
    return db.query(models.User).order_by(models.User.id).all()


@router.get("/{user_id}", response_model=schemas.User)
async def user_by_id(db: db_dependency, user_id: int):
    return get_user_by_id(db, user_id)


# PROFILE
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
