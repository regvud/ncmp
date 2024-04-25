from fastapi import APIRouter, Depends, UploadFile

import models
import schemas
from cross_related import delete_related_images
from db import db_dependency, delete_db_model, update_db_model
from enums import ImageTypeEnum
from permissions import authenticated_permission, owner_permission

from .crud import get_profile, get_user_by_id, upload_avatar, user_create

router = APIRouter(prefix="/users", tags=["Users"])


# PROFILE
@router.get("/profile", response_model=schemas.Profile)
async def user_profile(
    db: db_dependency,
    current_user: schemas.AuthenticatedUser = Depends(authenticated_permission),
):
    profile = get_profile(db, current_user.id)
    return profile


@router.put("/profile", response_model=schemas.Profile)
async def profile_update(
    db: db_dependency,
    updated_profile: schemas.ProfileUpdate,
    current_user: schemas.AuthenticatedUser = Depends(authenticated_permission),
):
    db_profile = get_profile(db, current_user.id)

    for k, v in updated_profile:
        setattr(db_profile, k, v)

    update_db_model(db, db_profile)
    return db_profile


@router.post("/profile/avatar", response_model=schemas.Avatar)
async def profile_change_avatar(
    db: db_dependency,
    file: UploadFile,
    current_user: schemas.AuthenticatedUser = Depends(authenticated_permission),
):
    created_avatar = upload_avatar(db=db, upload_file=file, user_id=current_user.id)
    return created_avatar


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


@router.delete("/{user_id}")
async def delete_user(
    db: db_dependency,
    user_id: int,
    current_user: schemas.AuthenticatedUser = Depends(owner_permission),
):
    user_to_delete = get_user_by_id(db, user_id)

    delete_related_images(ImageTypeEnum.AVATAR, user_id)
    delete_db_model(db, user_to_delete)
    return {"detail": f"Deleted user: {user_to_delete.email}"}
