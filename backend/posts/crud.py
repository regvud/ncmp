from fastapi import APIRouter, HTTPException

from backend import models, schemas
from backend.db import db_dependency, delete_db_model, save_db_model, update_db_model
from backend.users.crud import get_user_by_id

router = APIRouter(prefix="/posts", tags=["Posts"])


# POSTS
def get_post_by_id(db: db_dependency, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.post("/create", response_model=schemas.Post)
async def post_create(db: db_dependency, post: schemas.PostCreate):
    get_user_by_id(db, post.user_id)

    post = models.Post(**post.model_dump())
    save_db_model(db, post)
    return post


@router.get("/", response_model=list[schemas.Post])
async def posts(db: db_dependency):
    return db.query(models.Post).all()


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
def get_comment_by_id(db: db_dependency, comment_id: int):
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


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
