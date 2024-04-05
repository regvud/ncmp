from fastapi import FastAPI

from . import models
from .db import engine
from .posts.crud import router as post_router
from .users.crud import router as user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

routers = (user_router, post_router)

for router in routers:
    app.include_router(router)
