from fastapi import APIRouter, Depends

from content.crud import (get_like_counter_schema, user_like_create,
                          user_like_delete)
from db import db_dependency
from enums import ContentTypeEnum
from permissions import authenticated_permission
from schemas import AuthenticatedUser, Like, LikeCounter

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.get("/post/{post_id}", response_model=LikeCounter)
async def get_post_like(
    db: db_dependency,
    post_id: int,
):
    return get_like_counter_schema(
        db=db, content_type=ContentTypeEnum.POST, content_id=post_id
    )


@router.post("/post/{post_id}", response_model=Like)
async def post_user_like(
    db: db_dependency,
    post_id: int,
    current_user: AuthenticatedUser = Depends(authenticated_permission),
):
    return user_like_create(
        db=db,
        content_type=ContentTypeEnum.POST,
        content_id=post_id,
        user_id=current_user.id,
    )


@router.delete("/post/{post_id}")
async def post_user_like_delete(
    db: db_dependency,
    post_id: int,
    current_user: AuthenticatedUser = Depends(authenticated_permission),
):
    return user_like_delete(
        content_type=ContentTypeEnum.POST,
        db=db,
        content_id=post_id,
        user_id=current_user.id,
    )


@router.get("/comment/{comment_id}", response_model=LikeCounter)
async def get_comment_like(
    db: db_dependency,
    comment_id: int,
):
    return get_like_counter_schema(
        db=db, content_type=ContentTypeEnum.COMMENT, content_id=comment_id
    )


@router.post("/comment/{comment_id}", response_model=Like)
async def comment_user_like(
    db: db_dependency,
    comment_id: int,
    current_user: AuthenticatedUser = Depends(authenticated_permission),
):
    return user_like_create(
        db=db,
        content_type=ContentTypeEnum.COMMENT,
        content_id=comment_id,
        user_id=current_user.id,
    )


@router.delete("/comment/{comment_id}")
async def comment_user_like_delete(
    db: db_dependency,
    comment_id: int,
    current_user: AuthenticatedUser = Depends(authenticated_permission),
):
    return user_like_delete(
        db=db,
        content_type=ContentTypeEnum.COMMENT,
        content_id=comment_id,
        user_id=current_user.id,
    )


@router.get("/reply/{reply_id}", response_model=LikeCounter)
async def get_reply_like(
    db: db_dependency,
    reply_id: int,
):
    return get_like_counter_schema(
        db=db, content_type=ContentTypeEnum.REPLY, content_id=reply_id
    )


@router.post("/reply/{reply_id}", response_model=Like)
async def reply_user_like(
    db: db_dependency,
    reply_id: int,
    current_user: AuthenticatedUser = Depends(authenticated_permission),
):
    return user_like_create(
        db=db,
        content_type=ContentTypeEnum.REPLY,
        content_id=reply_id,
        user_id=current_user.id,
    )


@router.delete("/reply/{reply_id}")
async def reply_user_like_delete(
    db: db_dependency,
    reply_id: int,
    current_user: AuthenticatedUser = Depends(authenticated_permission),
):
    return user_like_delete(
        db=db,
        content_type=ContentTypeEnum.REPLY,
        content_id=reply_id,
        user_id=current_user.id,
    )
