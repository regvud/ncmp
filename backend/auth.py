from datetime import datetime, timedelta
from os import environ as env
from typing import Annotated

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

import models
import schemas
from config import CLIENT_ID, CLIENT_SECRET
from cross_related import pwd_context
from db import db_dependency
from exceptions import (
    TOKEN_EXPIRED_EXCEPTION,
    UNAUTHORIZED_EXCEPTION,
)
from users.crud import get_user_by_email, oauth_user_create

ACCESS_TOKEN_EXPIRE_MINUTES = 500
REFRESH_TOKEN_EXPIRE_MINUTES = 1000

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


router = APIRouter(prefix="/auth", tags=["Auth"])

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        "scope": "email openid profile",
        "redirect_url": "http://localhost:8000/auth",
    },
)


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


def authenticate_user(email: str, password: str, db: db_dependency):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=404, detail="User with given email doesn't exist"
        )
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=404, detail="Wrong password provided")
    return user


def create_token(email: str, user_id: int, is_owner: bool, expire_delta: timedelta):
    encode = {"email": email, "id": user_id, "is_owner": is_owner}
    expires = datetime.now() + expire_delta

    encode.update({"exp": expires.timestamp()})

    return jwt.encode(encode, env.get("SECRET_KEY"), algorithm=env.get("ALGORITHM"))


def generate_access_refresh_tokens(user: models.User):
    user_data = {"email": user.email, "user_id": user.id, "is_owner": user.is_owner}

    access = create_token(
        **user_data,
        expire_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh = create_token(
        **user_data,
        expire_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )
    return Tokens(access=access, refresh=refresh)


@router.post("/token", response_model=SwaggerToken)
async def swagger_token(
    user: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(user.email, user.password, db)

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
    user = authenticate_user(user.username, user.password, db)

    token_pair = generate_access_refresh_tokens(user)
    return token_pair


@router.get("/google-login")
async def google_login(request: Request):
    url = request.url_for("google_auth")
    return await oauth.google.authorize_redirect(request, url)


@router.get("/google-auth")
async def google_auth(db: db_dependency, request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return HTTPException(status_code=404, detail=f"google auth error: {e}")

    user_info = token.get("userinfo")
    user_email = user_info.get("email")

    db_user = get_user_by_email(db, user_email)

    if db_user:
        token_pair = generate_access_refresh_tokens(db_user)
        return token_pair

    created_user = oauth_user_create(db, user_info)

    token_pair = generate_access_refresh_tokens(created_user)
    return token_pair


@router.post("/refresh")
async def refresh_tokens(db: db_dependency, token: RefreshTokenModel):
    payload = decoder(token.refresh_token)
    user = get_user_by_email(db, payload.get("email"))

    token_pair = generate_access_refresh_tokens(user)
    return token_pair


@router.get("/me/", response_model=schemas.User)
async def me(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    payload = decoder(token)
    email = payload.get("email")

    current_user = get_user_by_email(db, email)
    if not current_user:
        raise UNAUTHORIZED_EXCEPTION
    return current_user
