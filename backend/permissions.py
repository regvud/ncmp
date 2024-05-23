from typing import Optional

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from auth import decoder, oauth2_scheme
from content.crud import get_comment_by_id, get_post_by_id, get_reply_by_id
from db import db_dependency
from enums import ContentTypeEnum
from exceptions import TOKEN_EXPIRED_EXCEPTION, not_owner_exception
import models
from schemas import AuthenticatedUser


def check_ownership(
    db: db_dependency, user_id: int, content_type: ContentTypeEnum, content_id: int
):
    match content_type:
        case ContentTypeEnum.POST:
            post = get_post_by_id(db, content_id)
            if not post.user_id == user_id:
                raise not_owner_exception(ContentTypeEnum.POST)
        case ContentTypeEnum.COMMENT:
            comment = get_comment_by_id(db, content_id)
            if not comment.user_id == user_id:
                raise not_owner_exception(ContentTypeEnum.COMMENT)
        case ContentTypeEnum.REPLY:
            reply = get_reply_by_id(db, content_id)
            if not reply.user_id == user_id:
                raise not_owner_exception(ContentTypeEnum.REPLY)
    return None


def authenticated_permission(token: str = Depends(oauth2_scheme)):
    payload = decoder(token)
    print(payload)
    email: str = payload.get("email")
    if email is None:
        raise TOKEN_EXPIRED_EXCEPTION

    auth_user = AuthenticatedUser(**payload)
    return auth_user


def owner_permission(token: str = Depends(oauth2_scheme)):
    auth_user = authenticated_permission(token)
    if not auth_user.is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owner allowed to perform this action",
        )
    return auth_user


class DeletionContext(BaseModel):
    token: str = Depends(oauth2_scheme)
    reply_id: Optional[int] = None
    comment_id: Optional[int] = None
    post_id: Optional[int] = None


def delete_permission(
    db: db_dependency,
    context: DeletionContext = Depends(),
):
    auth_user = authenticated_permission(context.token)

    if auth_user.is_owner:
        return auth_user

    if context.comment_id:
        db_comment = (
            db.query(models.Comment)
            .filter(models.Comment.id == context.comment_id)
            .first()
        )
        if db_comment and db_comment.user_id != auth_user.id:
            raise not_owner_exception(ContentTypeEnum.COMMENT)

    if context.reply_id:
        db_reply = (
            db.query(models.Reply).filter(models.Reply.id == context.reply_id).first()
        )

        if db_reply and db_reply.user_id != auth_user.id:
            raise not_owner_exception(ContentTypeEnum.REPLY)

    return auth_user
