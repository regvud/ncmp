from fastapi import HTTPException, status

import models
from db import db_dependency
from enums import ContentTypeEnum
from exceptions import not_owner_exception


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


# REPLIESS
def get_reply_by_id(db: db_dependency, reply_id: int):
    db_reply = db.query(models.Reply).filter(models.Reply.id == reply_id).first()

    if not db_reply:
        raise HTTPException(status_code=404, detail="Reply not found")
    return db_reply
