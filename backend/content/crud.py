from fastapi import HTTPException, UploadFile
from sqlalchemy.orm.strategy_options import joinedload

import models
from cross_related import uuid_creator, write_image_file
from db import db_dependency, delete_db_model, print_query_count, save_db_model
from enums import ContentTypeEnum, NotificationTypeEnum
from exceptions import liked_exception, unliked_exception
from schemas import LikeCounter, PostCounterSchema
from users.crud import get_profile, get_user_by_id


# POSTS
def filter_popper(idx: int, iterable: list):
    filtered_obj = list(filter(lambda like: like.content_id == idx, iterable))[0]
    like_idx = iterable.index(filtered_obj)
    iterable.pop(like_idx)
    return filtered_obj


def test_ul(db: db_dependency):
    q = (
        db.query(models.UserLike, models.User)
        .join(models.User)
        .filter(models.UserLike.like_id == 24)
        .all()
    )
    for like, user in q:
        print(like.user_id, user.id)


def get_posts_with_counters(
    db: db_dependency, posts: list[models.Post]
) -> list[PostCounterSchema]:

    query_likes = db.query(models.Like).all()

    likes_by_content_type = {
        ContentTypeEnum.POST: [],
        ContentTypeEnum.COMMENT: [],
        ContentTypeEnum.REPLY: [],
    }

    for like in query_likes:
        likes_by_content_type[like.content_type].append(like)

    post_likes = likes_by_content_type[ContentTypeEnum.POST]
    comment_likes = likes_by_content_type[ContentTypeEnum.COMMENT]
    reply_likes = likes_by_content_type[ContentTypeEnum.REPLY]

    post_schemas = []
    for post in posts:
        cnt_like = filter_popper(post.id, post_likes)

        like_user_query = (
            db.query(models.UserLike, models.User)
            .join(models.User)
            .filter(models.UserLike.like_id == 24)
            .all()
        )

        post_like_ids = {
            (u.id, u.profile.avatar.avatar if u.profile.avatar else "")
            for _, u in like_user_query[:3]
        }

        post_images = [image.__dict__ for image in post.images]

        post_comments = []
        for comment in post.comments:
            cnt_like = filter_popper(comment.id, comment_likes)
            comment_like_ids = {ul.user_id for ul in cnt_like.users_liked}

            comment_replies = []
            for reply in comment.replies:
                cnt_like = filter_popper(reply.id, reply_likes)
                reply_like_ids = {ul.user_id for ul in cnt_like.users_liked}

                reply_dict = reply.__dict__.copy()
                reply_dict.update(
                    {"likes_count": len(reply_like_ids), "users_liked": reply_like_ids}
                )
                comment_replies.append(reply_dict)

            comment_dict = comment.__dict__.copy()
            comment_dict.update(
                {
                    "replies_count": len(comment_replies),
                    "replies": comment_replies,
                    "likes_count": len(comment_like_ids),
                    "users_liked": comment_like_ids,
                }
            )
            post_comments.append(comment_dict)

        post_dict = post.__dict__.copy()
        post_dict.update(
            {
                "comments_count": len(post_comments),
                "images": post_images,
                "likes_count": len(like_user_query),
                "users_liked": post_like_ids,
                "comments": post_comments,
            }
        )

        print_query_count()
        post_schemas.append(PostCounterSchema(**post_dict))

    return post_schemas


def get_post_by_id(db: db_dependency, post_id: int) -> models.Post:
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


def upload_post_images(db: db_dependency, post_id: int, image_files: list[UploadFile]):
    for image_file in image_files:
        uu_filename = uuid_creator(image_file.filename, str(post_id))
        path_to_file = f"images/posts/{uu_filename}"

        write_image_file(image_file, path_to_file)

        new_post_image = models.PostImage(post_id=post_id, path=f"/{path_to_file}")
        save_db_model(db, new_post_image)


# COMMENTS
def get_comment_by_id(db: db_dependency, comment_id: int) -> models.Comment:
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


def message_notification(notification_type: str, from_user: models.User):
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
    content_id: int,
    user_id: int,
):
    content_like = get_like_by_id(db, content_type, content_id)
    db_user_like = get_user_like(db, user_id, content_like.id)

    if db_user_like:
        raise liked_exception(content_type)

    data = {"like_id": content_like.id, "user_id": user_id}
    user_like = models.UserLike(**data)
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
                notification = models.Notification(**notification_data)
                save_db_model(db, notification)

        case ContentTypeEnum.REPLY:
            reply = get_reply_by_id(db, content_id)

            if current_user.id != reply.to_user:
                notification_data.update({"profile_id": reply.to_user})
                notification = models.Notification(**notification_data)
                save_db_model(db, notification)

        case ContentTypeEnum.COMMENT:
            comment = get_comment_by_id(db, content_id)

            if current_user.id != comment.user_id:
                notification_data.update({"profile_id": f"{comment.user_id}"})
                notification = models.Notification(**notification_data)
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
    db: db_dependency, content_type: ContentTypeEnum, content_id: int
):
    like = get_like_by_id(db, content_type, content_id)

    like_dict = like.__dict__
    users_liked_ids: set[int] = {user_like.user_id for user_like in like.users_liked}

    like_dict.update({"users_liked": users_liked_ids, "count": len(users_liked_ids)})

    like_counter_schema = LikeCounter(**like_dict)
    return like_counter_schema
