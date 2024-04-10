from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# USER RELATED
class UserBase(BaseModel):
    email: str


class AuthenticatedUser(UserBase):
    id: int
    exp: float
    is_owner: bool


class UserCreate(UserBase):
    password: str
    is_owner: Optional[bool] = False


class User(UserBase):
    id: int
    is_active: bool
    is_owner: bool
    profile: "Profile"
    posts: list["PostNoComments"] = []
    comments: list["Comment"] = []

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ProfileBase(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None


class ProfileUpdate(ProfileBase):
    pass


class Profile(ProfileUpdate):
    id: int

    user_id: int
    avatar: Optional["Avatar"] = None

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class AvatarBase(BaseModel):
    profile_id: int
    avatar: bytes | None


class Avatar(AvatarBase):
    id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


# POST RELATED
class PostBase(BaseModel):
    title: str
    body: str


class PostUpdate(PostBase):
    pass


class PostCreate(PostBase):
    pass


class Post(PostCreate):
    id: int
    user_id: int
    comments: list["Comment"] = []


class PostNoComments(PostCreate):
    id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class CommentBase(BaseModel):
    body: str


class CommentUpdate(CommentBase):
    pass


class CommentCreate(CommentBase):
    pass


class Comment(CommentCreate):
    id: int

    post_id: int
    user_id: int
    replies: list["Reply"] = []

    created_at: Optional[datetime]
    updated_at: Optional[datetime]


# REPLIES
class ReplyBase(BaseModel):
    body: str


class ReplyUpdate(ReplyBase):
    pass


class ReplyCreate(ReplyBase):
    pass


class Reply(ReplyCreate):
    id: int

    to_user: int
    user_id: int

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
