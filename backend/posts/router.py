from fastapi import APIRouter, Depends

import models
import schemas
from auth import authenticated_permission, owner_permission
from db import db_dependency, delete_db_model, save_db_model, update_db_model
from users.crud import get_user_by_id

from .crud import get_comment_by_id, get_post_by_id

router = APIRouter(prefix="/posts", tags=["Posts"])


# POSTS
@router.post("/create", response_model=schemas.Post)
async def post_create(
    db: db_dependency,
    post: schemas.PostCreate,
    current_user: schemas.AuthenticatedUser = Depends(owner_permission),
):
    post = models.Post(**post.model_dump(), user_id=current_user.id)
    save_db_model(db, post)
    return post


@router.get("/", response_model=list[schemas.Post])
async def posts(db: db_dependency):
    return db.query(models.Post).order_by(models.Post.id).all()


@router.get("/{post_id}", response_model=schemas.Post)
async def post_by_id(db: db_dependency, post_id: int):
    return get_post_by_id(db, post_id)


@router.put("/{post_id}", response_model=schemas.Post)
async def post_put(db: db_dependency, post_id: int, updated_post: schemas.PostUpdate):
    db_post = get_post_by_id(db, post_id)

    for key, value in updated_post.model_dump().items():
        setattr(db_post, key, value)

    update_db_model(db, db_post)
    return db_post


@router.delete("/{post_id}")
async def post_delete(db: db_dependency, post_id: int):
    post_to_delete = get_post_by_id(db, post_id)

    delete_db_model(db, post_to_delete)
    return {"detail": f"Post {post_id} deleted successfully"}


# COMMENTS
@router.post("/{post_id}/comment", response_model=schemas.Comment)
async def comment_create(db: db_dependency, comment: schemas.CommentCreate):
    get_post_by_id(db, comment.post_id)
    get_user_by_id(db, comment.user_id)

    comment = models.Comment(**comment.model_dump())
    save_db_model(db, comment)
    return comment


@router.get("/comment/{comment_id}", response_model=schemas.Comment)
async def comment_by_id(db: db_dependency, comment_id: int):
    return get_comment_by_id(db, comment_id)


@router.put("/comment/{comment_id}", response_model=schemas.Comment)
async def comment_put(
    db: db_dependency, comment_id: int, updated_comment: schemas.CommentUpdate
):
    db_comment = get_comment_by_id(db, comment_id)

    for k, v in updated_comment.model_dump().items():
        setattr(db_comment, k, v)

    update_db_model(db, db_comment)
    return db_comment


@router.delete("/comment/{comment_id}")
async def comment_delete(db: db_dependency, comment_id: int):
    comment_to_delete = get_comment_by_id(db, comment_id)

    delete_db_model(db, comment_to_delete)
    return {"detail": f"Comment {comment_id} deleted successfully"}


# REPLIES
@router.post("/comment/{comment_id}/reply", response_model=schemas.Reply)
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
        "from_user": current_user.id,
        "to_user": comment.user_id,
    }

    reply = models.Reply(**data)
    return reply
