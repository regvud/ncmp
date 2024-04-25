import pathlib

from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse

import models
from auth import router as auth_router
from content.comments.router import router as comment_router
from content.likes.router import router as like_router
from content.notifications.router import router as notif_router
from content.posts.router import router as post_router
from content.replies.router import router as reply_router
from db import engine
from exceptions import FILE_NOT_FOUND_EXCEPTION
from products.router import router as product_router
from users.router import router as user_router

AVATARS_PATH = "images/avatars"
POST_IMAGES_PATH = "images/posts"

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app_router = APIRouter(tags=["View Images"])


@app_router.get("/images/avatars/{file_name}")
async def view_avatar(file_name: str):
    matched_files = list(pathlib.Path(AVATARS_PATH).glob(file_name))
    if not matched_files:
        raise FILE_NOT_FOUND_EXCEPTION

    return FileResponse(matched_files[0])


@app_router.get("/images/posts/{file_name}")
async def view_image(file_name: str):
    matched_files = list(pathlib.Path(POST_IMAGES_PATH).glob(file_name))
    if not matched_files:
        raise FILE_NOT_FOUND_EXCEPTION

    return FileResponse(matched_files[0])


routers = (
    app_router,
    auth_router,
    user_router,
    post_router,
    comment_router,
    reply_router,
    like_router,
    notif_router,
    product_router,
)


for router in routers:
    app.include_router(router)
