from fastapi import APIRouter, Depends

from content.crud import (
    create_related_like_notification_models,
    get_comment_by_id,
    get_post_by_id,
)
from cross_related import delete_related_db_models
from db import db_dependency, delete_db_model, save_db_model, update_db_model
from enums import ContentTypeEnum, NotificationTypeEnum
import models
from permissions import authenticated_permission, check_ownership, delete_permission
import schemas


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/post/{post_id}", response_model=schemas.Comment)
async def comment_create(
    db: db_dependency,
    post_id: int,
    comment: schemas.CommentCreate,
    current_user: schemas.AuthenticatedUser = Depends(authenticated_permission),
):
    post = get_post_by_id(db, post_id)

    comment = models.Comment(
        **comment.model_dump(), post_id=post_id, user_id=current_user.id
    )

    save_db_model(db, comment)

    create_related_like_notification_models(
        db=db,
        content_type=ContentTypeEnum.COMMENT,
        notification_type=NotificationTypeEnum.COMMENT,
        content_id=comment.id,
        current_user_id=current_user.id,
        user_to_notify_id=post.user_id,
    )
    return comment


@router.get("/{comment_id}", response_model=schemas.Comment)
async def comment_by_id(db: db_dependency, comment_id: int):
    return get_comment_by_id(db, comment_id)


@router.put("/{comment_id}", response_model=schemas.Comment)
async def comment_put(
    db: db_dependency,
    comment_id: int,
    updated_comment: schemas.CommentUpdate,
    current_user: schemas.AuthenticatedUser = Depends(authenticated_permission),
):
    check_ownership(
        db=db,
        user_id=current_user.id,
        content_type=ContentTypeEnum.COMMENT,
        content_id=comment_id,
    )

    db_comment = get_comment_by_id(db, comment_id)

    for k, v in updated_comment.model_dump().items():
        setattr(db_comment, k, v)

    update_db_model(db, db_comment)
    return db_comment


@router.delete("/{comment_id}")
async def comment_delete(
    db: db_dependency,
    comment_id: int,
    current_user: schemas.AuthenticatedUser = Depends(delete_permission),
):
    comment_to_delete = get_comment_by_id(db, comment_id)

    delete_related_db_models(db, comment_id, ContentTypeEnum.COMMENT)
    delete_db_model(db, comment_to_delete)
    return {"detail": f"Comment {comment_id} deleted successfully"}
