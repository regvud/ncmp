from fastapi import APIRouter, Depends, UploadFile

import models
import schemas
from content.crud import (
    get_post_by_id,
    upload_post_images,
)
from db import db_dependency, delete_db_model, save_db_model, update_db_model
from enums import ContentTypeEnum
from permissions import owner_permission

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/create", response_model=schemas.Post)
async def post_create(
    db: db_dependency,
    post: schemas.PostCreate,
    current_user: schemas.AuthenticatedUser = Depends(owner_permission),
):
    post = models.Post(**post.model_dump(), user_id=current_user.id)
    save_db_model(db, post)

    like = models.Like(content_id=post.id, content_type=ContentTypeEnum.POST)

    save_db_model(db, like)
    return post


@router.get("/", response_model=list[schemas.Post])
async def posts(db: db_dependency):
    return db.query(models.Post).order_by(models.Post.id).all()


@router.get("/{post_id}", response_model=schemas.Post)
async def post_by_id(db: db_dependency, post_id: int):
    return get_post_by_id(db, post_id)


@router.put("/{post_id}", response_model=schemas.Post)
async def post_put(
    db: db_dependency,
    post_id: int,
    updated_post: schemas.PostUpdate,
    current_user: schemas.AuthenticatedUser = Depends(owner_permission),
):
    db_post = get_post_by_id(db, post_id)

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    update_db_model(db, db_post)
    return db_post


@router.delete("/{post_id}")
async def post_delete(
    db: db_dependency,
    post_id: int,
    current_user: schemas.AuthenticatedUser = Depends(owner_permission),
):
    post_to_delete = get_post_by_id(db, post_id)

    delete_db_model(db, post_to_delete)
    return {"detail": f"Post {post_id} deleted successfully"}


@router.post("/{post_id}/images", response_model=list[schemas.PostImageSchema])
async def post_add_images(db: db_dependency, images: list[UploadFile], post_id: int):
    upload_post_images(db, post_id, images)
    post_images = db.query(models.PostImage).filter(models.PostImage.post_id == post_id)

    return [image.__dict__ for image in post_images]
