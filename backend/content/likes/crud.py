from fastapi import HTTPException

from content.crud import (
    get_comment_by_id,
    get_post_by_id,
    get_reply_by_id,
    message_notification,
)
from db import db_dependency, delete_db_model, save_db_model
from enums import ContentTypeEnum, NotificationTypeEnum
from exceptions import liked_exception, unliked_exception
from models import Like, Notification, UserLike
from schemas import LikeCounter
from users.crud import get_user_by_id


def get_like_by_id(db: db_dependency, content_type: ContentTypeEnum, content_id: int):
    db_like = (
        db.query(Like)
        .filter(Like.content_id == content_id)
        .filter(Like.content_type == content_type)
        .first()
    )

    if not db_like:
        raise HTTPException(status_code=404, detail="Like not found")

    return db_like


def get_user_like(db: db_dependency, user_id: int, like_id: int):
    user_like = (
        db.query(UserLike)
        .filter(UserLike.user_id == user_id)
        .filter(UserLike.like_id == like_id)
        .first()
    )

    return user_like


def user_like_create(
    db: db_dependency,
    content_type: ContentTypeEnum,
    content_id: int,
    user_id: int,
):
    content_like = get_like_by_id(db, content_type, content_id)
    db_user_like = get_user_like(db, user_id, content_like.id)

    if db_user_like:
        raise liked_exception(content_type)

    user_like = UserLike(like_id=content_like.id, user_id=user_id)
    current_user = get_user_by_id(db, user_id)

    notification_data = {
        "type": NotificationTypeEnum.LIKE,
        "message": message_notification(NotificationTypeEnum.LIKE.value, current_user),
    }

    match content_type:
        case ContentTypeEnum.POST:
            post = get_post_by_id(db, content_id)

            if current_user.id != post.user_id:
                notification_data.update({"profile_id": f"{post.user_id}"})
                notification = Notification(**notification_data)
                save_db_model(db, notification)

        case ContentTypeEnum.REPLY:
            reply = get_reply_by_id(db, content_id)

            if current_user.id != reply.to_user:
                notification_data.update({"profile_id": f"{reply.to_user}"})
                notification = Notification(**notification_data)
                save_db_model(db, notification)

        case ContentTypeEnum.COMMENT:
            comment = get_comment_by_id(db, content_id)

            if current_user.id != comment.user_id:
                notification_data.update({"profile_id": f"{comment.user_id}"})
                notification = Notification(**notification_data)
                save_db_model(db, notification)

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
        db.query(UserLike)
        .filter(UserLike.user_id == user_id)
        .filter(UserLike.like_id == like.id)
    ).count()

    like_dict = like.__dict__

    users_liked_ids: set[int] = {user_like.user_id for user_like in like.users_liked}

    like_dict.update({"users_liked": users_liked_ids})

    like_counter_schema = LikeCounter(**like_dict, count=count)
    return like_counter_schema
