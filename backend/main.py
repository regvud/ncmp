from fastapi import FastAPI

from . import models
from .db import engine
from .users.crud import router as user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)
