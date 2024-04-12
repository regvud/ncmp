from fastapi import FastAPI

import models
from auth import router as auth_router
from content.comments.router import router as comment_router
from content.likes.router import router as like_router
from content.posts.router import router as post_router
from content.replies.router import router as reply_router
from db import engine
from users.router import router as user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

routers = (
    auth_router,
    user_router,
    post_router,
    comment_router,
    reply_router,
    like_router,
)

for router in routers:
    app.include_router(router)
