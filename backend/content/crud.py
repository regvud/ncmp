from fastapi import HTTPException, UploadFile

import models
from cross_related import uuid_creator, write_image_file
from db import db_dependency, delete_db_model, save_db_model
from enums import ContentTypeEnum, NotificationTypeEnum
from exceptions import not_owner_exception
from users.crud import get_profile, get_user_by_id


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
def get_post_by_id(db: db_dependency, post_id: int) -> models.Post:
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


def upload_post_images(db: db_dependency, post_id: int, image_files: list[UploadFile]):
    for image_file in image_files:
        uu_filename = uuid_creator(image_file.filename, post_id)
        path_to_file = f"images/posts/{uu_filename}"

        write_image_file(image_file, path_to_file)

        new_post_image = models.PostImage(post_id=post_id, path=f"/{path_to_file}")
        save_db_model(db, new_post_image)


def post_handle_comment_count(db: db_dependency, post_id: int, action: bool):
    post = get_post_by_id(db, post_id)

    if action:
        post.comments_count += 1
    else:
        post.comments_count -= 1

    db.commit()
    db.refresh(post)


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


# NOTIFICATIONS
def get_user_notifications(db: db_dependency, user_id: int):
    user_profile_id = get_profile(db, user_id).id

    user_notifications = (
        db.query(models.Notification)
        .filter(models.Notification.profile_id == user_profile_id)
        .all()
    )

    return user_notifications


def notification_delete(db: db_dependency, notification_id: int):
    notification_to_delete = (
        db.query(models.Notification)
        .filter(models.Notification.id == notification_id)
        .first()
    )
    delete_db_model(db, notification_to_delete)

    return {"detail": f"Deleted notification {notification_id}"}


def read_notifications(db: db_dependency, user_id: int) -> bool:
    user_profile_id = get_profile(db, user_id).id

    query = (
        db.query(models.Notification)
        .filter(models.Notification.profile_id == user_profile_id)
        .filter(models.Notification.status.is_(False))
    )

    if query.all() == []:
        return False

    query.update({models.Notification.status: True})

    db.commit()

    return True


def message_notification(
    notification_type: NotificationTypeEnum, from_user: models.User
):
    return f"You have new {notification_type} from user {from_user.email}"


def create_related_like_notification_models(
    db: db_dependency,
    content_type: ContentTypeEnum,
    notification_type: NotificationTypeEnum,
    content_id: int,
    current_user_id: int,
    user_to_notify_id: int,
):
    """
    attaches likes_model to created object,
    attaches notif_model only if current_user != notify_user
    """

    notify_user = get_user_by_id(db, user_to_notify_id)
    current_user = get_user_by_id(db, current_user_id)

    like = models.Like(content_id=content_id, content_type=content_type)

    if current_user_id != user_to_notify_id:
        notification = models.Notification(
            profile_id=notify_user.profile.id,
            type=notification_type,
            message=message_notification(notification_type.value, current_user),
        )
        save_db_model(db, notification)

    save_db_model(db, like)
