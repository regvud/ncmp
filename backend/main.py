import pathlib

from fastapi import FastAPI
from fastapi.responses import FileResponse

import models
from auth import router as auth_router
from content.comments.router import router as comment_router
from content.likes.router import router as like_router
from content.notifications.router import router as notif_router
from content.posts.router import router as post_router
from content.replies.router import router as reply_router
from db import engine
from users.router import router as user_router

AVATARS_PATH = "images/"

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

routers = (
    auth_router,
    user_router,
    post_router,
    comment_router,
    reply_router,
    like_router,
    notif_router,
)

for router in routers:
    app.include_router(router)


@app.router.get("/images/avatars/{file_name}")
async def view_image(file_name: str):
    path = pathlib.Path(AVATARS_PATH).glob(f"**/*{file_name}").__next__()
    return FileResponse(path)
