from typing import Optional

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

import models
from auth import decoder, oauth2_scheme
from db import db_dependency
from enums import ContentTypeEnum
from exceptions import TOKEN_EXPIRED_EXCEPTION, not_owner_exception
from schemas import AuthenticatedUser


def authenticated_permission(token: str = Depends(oauth2_scheme)):
    payload = decoder(token)
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
            raise not_owner_exception(ContentTypeEnum.COMMENT.value)

    if context.reply_id:
        db_reply = (
            db.query(models.Reply).filter(models.Reply.id == context.reply_id).first()
        )

        if db_reply and db_reply.user_id != auth_user.id:
            raise not_owner_exception(ContentTypeEnum.REPLY.value)

    return auth_user
