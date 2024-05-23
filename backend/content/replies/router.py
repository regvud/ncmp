from fastapi import APIRouter, Depends

from content.crud import (
    create_related_like_notification_models,
    get_comment_by_id,
    get_reply_by_id,
)
from cross_related import delete_related_db_models
from db import db_dependency, delete_db_model, save_db_model, update_db_model
from enums import ContentTypeEnum, NotificationTypeEnum
import models
from permissions import authenticated_permission, delete_permission, check_ownership
import schemas

router = APIRouter(prefix="/replies", tags=["Replies"])


@router.post("/comment/{comment_id}", response_model=schemas.Reply)
async def reply_create(
    db: db_dependency,
    comment_id: int,
    reply: schemas.ReplyCreate,
    current_user: schemas.AuthenticatedUser = Depends(authenticated_permission),
):
    comment = get_comment_by_id(db, comment_id)

    data = {
        "body": reply.body,
        "comment_id": comment_id,
        "user_id": current_user.id,
        "to_user": comment.user_id,
    }

    new_reply = models.Reply(**data)
    save_db_model(db, new_reply)

    create_related_like_notification_models(
        db=db,
        content_type=ContentTypeEnum.REPLY,
        notification_type=NotificationTypeEnum.REPLY,
        content_id=new_reply.id,
        current_user_id=current_user.id,
        user_to_notify_id=new_reply.to_user,
    )

    return new_reply


@router.get("/{reply_id}", response_model=schemas.Reply)
async def reply_get(db: db_dependency, reply_id: int):
    return get_reply_by_id(db, reply_id)


@router.put("/{reply_id}", response_model=schemas.Reply)
async def reply_put(
    db: db_dependency,
    reply_id: int,
    reply: schemas.ReplyUpdate,
    current_user: schemas.AuthenticatedUser = Depends(authenticated_permission),
):
    check_ownership(
        db=db,
        user_id=current_user.id,
        content_type=ContentTypeEnum.REPLY,
        content_id=reply_id,
    )

    db_reply = get_reply_by_id(db, reply_id)

    for k, v in reply:
        setattr(db_reply, k, v)

    update_db_model(db, db_reply)
    return db_reply


@router.delete("/{reply_id}")
async def reply_delete(
    db: db_dependency,
    reply_id: int,
    current_user: schemas.AuthenticatedUser = Depends(delete_permission),
):
    reply_to_delete = get_reply_by_id(db, reply_id)
    delete_related_db_models(db, reply_id, ContentTypeEnum.REPLY)
    delete_db_model(db, reply_to_delete)
    return {"detail": f"Reply {reply_id} deleted successfully"}
