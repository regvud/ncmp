from datetime import datetime, timedelta
from os import environ as env
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

import models
import schemas
from cross_related import pwd_context
from db import db_dependency
from exceptions import (
    TOKEN_EXPIRED_EXCEPTION,
    UNAUTHORIZED_EXCEPTION,
)
from users.crud import get_user_by_email

ACCESS_TOKEN_EXPIRE_MINUTES = 500
REFRESH_TOKEN_EXPIRE_MINUTES = 1000

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


router = APIRouter(prefix="/auth", tags=["Auth"])


class Tokens(BaseModel):
    access: str
    refresh: str


class SwaggerToken(BaseModel):
    access_token: str
    token_type: str


class RefreshTokenModel(BaseModel):
    refresh_token: str


def decoder(token: str):
    try:
        decoded_token = jwt.decode(
            token, env.get("SECRET_KEY"), algorithms=[env.get("ALGORITHM")]
        )
    except JWTError:
        raise TOKEN_EXPIRED_EXCEPTION

    return decoded_token


def authenticate_user(email: str, password: str, db):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def create_token(email: str, user_id: int, is_owner: bool, expire_delta: timedelta):
    encode = {"email": email, "id": user_id, "is_owner": is_owner}
    expires = datetime.now() + expire_delta

    encode.update({"exp": expires.timestamp()})

    return jwt.encode(encode, env.get("SECRET_KEY"), algorithm=env.get("ALGORITHM"))


@router.post("/token", response_model=SwaggerToken)
async def swagger_token(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(user.email, user.password, db)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user credentials, re-check email or password.",
        )

    access = create_token(
        user.email,
        user.id,
        user.is_owner,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access, "token_type": "bearer"}


@router.post("/login", response_model=Tokens)
async def login(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(user.email, user.password, db)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user credentials, re-check email or password.",
        )

    access = create_token(
        user.email,
        user.id,
        user.is_owner,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh = create_token(
        user.email,
        user.id,
        user.is_owner,
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )

    token_pair = Tokens(access=access, refresh=refresh)
    return token_pair


@router.post("/refresh")
async def refresh_tokens(token: RefreshTokenModel):
    payload = decoder(token.refresh_token)

    access = create_token(
        payload.get("email"),
        payload.get("id"),
        payload.get("is_owner"),
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh = create_token(
        payload.get("email"),
        payload.get("id"),
        payload.get("is_owner"),
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )

    return {"access": access, "refresh": refresh}


@router.get("/me/", response_model=schemas.User)
async def me(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    payload = decoder(token)
    email = payload.get("email")

    current_user = get_user_by_email(db, email)
    if not current_user:
        raise UNAUTHORIZED_EXCEPTION
    return current_user
