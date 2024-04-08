import models
from auth import router as auth_router
from db import engine
from fastapi import FastAPI
from posts.router import router as post_router
from users.router import router as user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

routers = (auth_router, user_router, post_router)

for router in routers:
    app.include_router(router)
