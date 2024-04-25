from fastapi import HTTPException, UploadFile

import models
import schemas
from cross_related import pwd_context, uuid_creator, write_image_file
from db import db_dependency, save_db_model


# USER
def get_user_by_email(db: db_dependency, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    return db_user


def get_user_by_id(db: db_dependency, id: int):
    db_user = db.query(models.User).filter(models.User.id == id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def user_create(db: db_dependency, user: schemas.UserCreate):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(status_code=404, detail="User already exist")

    hashed_password = pwd_context.hash(user.password)

    user.password = hashed_password

    profile = models.Profile()
    new_user = models.User(**user.model_dump(), profile=profile)

    save_db_model(db, new_user)
    return new_user


# PROFILE
def get_profile(db: db_dependency, user_id: int):
    db_profile = (
        db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    )

    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


def upload_avatar(
    db: db_dependency,
    user_id: int,
    upload_file: UploadFile,
):
    uu_filename = uuid_creator(upload_file.filename, user_id)

    path_to_file = f"images/avatars/{uu_filename}"

    write_image_file(upload_file, path_to_file)

    profile_id = get_profile(db, user_id).id

    db.query(models.ProfileAvatar).filter(
        models.ProfileAvatar.profile_id == profile_id
    ).delete()

    new_avatar = models.ProfileAvatar(profile_id=profile_id, avatar=f"/{path_to_file}")
    save_db_model(db, new_avatar)

    return new_avatar
