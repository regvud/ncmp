from fastapi import HTTPException

import models
import schemas
from db import db_dependency, delete_db_model, save_db_model
from enums import ContentTypeEnum
from exceptions import liked_exception, not_owner_exception, unliked_exception


def check_ownership(
    db: db_dependency, user_id: int, content_type: str, content_id: int
):
    match content_type:
        case ContentTypeEnum.POST:
            post = get_post_by_id(db, content_id)
            if not post.user_id == user_id:
                raise not_owner_exception(ContentTypeEnum.Post)
        case ContentTypeEnum.COMMENT:
            comment = get_comment_by_id(db, content_id)
            if not comment.user_id == user_id:
                raise not_owner_exception(ContentTypeEnum.COMMENT)
        case ContentTypeEnum.REPLY:
            reply = get_reply_by_id(db, content_id)
            if not reply.user_id == user_id:
                raise not_owner_exception(ContentTypeEnum.REPLY)
    return None


# POSTS
def get_post_by_id(db: db_dependency, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


# COMMENTS
def get_comment_by_id(db: db_dependency, comment_id: int):
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


# REPLIES
def get_reply_by_id(db: db_dependency, reply_id: int):
    db_reply = db.query(models.Reply).filter(models.Reply.id == reply_id).first()

    if not db_reply:
        raise HTTPException(status_code=404, detail="Reply not found")
    return db_reply


# LIKES
def get_like_by_id(db: db_dependency, content_type: ContentTypeEnum, content_id: int):
    db_like = (
        db.query(models.Like)
        .filter(models.Like.content_id == content_id)
        .filter(models.Like.content_type == content_type)
        .first()
    )

    if not db_like:
        raise HTTPException(status_code=404, detail="Like not found")

    return db_like


def get_user_like(db: db_dependency, user_id: int, like_id: int):
    user_like = (
        db.query(models.UserLike)
        .filter(models.UserLike.user_id == user_id)
        .filter(models.UserLike.like_id == like_id)
        .first()
    )

    return user_like


def user_like_create(
    db: db_dependency,
    content_type: ContentTypeEnum,
    content_id,
    user_id: int,
):
    content_like = get_like_by_id(db, content_type, content_id)

    db_user_like = get_user_like(db, user_id, content_like.id)

    if db_user_like:
        raise liked_exception(content_type)

    user_like = models.UserLike(like_id=content_like.id, user_id=user_id)
    save_db_model(db, user_like)

    return content_like


def user_like_delete(
    db: db_dependency, content_type: ContentTypeEnum, content_id: int, user_id: int
):
    db_like = get_like_by_id(db, content_type, content_id)

    user_like_to_delete = get_user_like(db, user_id, db_like.id)
    if not user_like_to_delete:
        raise unliked_exception(content_type)

    delete_db_model(db, user_like_to_delete)
    return {"detail": f"Deleted like {user_like_to_delete.id}"}


def get_like_counter_schema(
    db: db_dependency, content_type: ContentTypeEnum, content_id: int, user_id: int
):
    like = get_like_by_id(db, content_type, content_id)

    count = (
        db.query(models.UserLike)
        .filter(models.UserLike.user_id == user_id)
        .filter(models.UserLike.like_id == like.id)
    ).count()

    like_dict = like.__dict__
    like_dict.update({"count": count})
    like_dict.update({"users_liked": []})

    users_liked: list = like_dict.get("users_liked")

    users = like.users_liked.all()

    for user in users:
        users_liked.append({"user_id": user.user_id})

    like_counter_schema = schemas.LikeCounter(
        **like_dict,
    )

    return like_counter_schema
