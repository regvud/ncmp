from typing import Optional

from pydantic import BaseModel


# USER RELATED
class UserBase(BaseModel):
    email: str


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


class ProfileBase(BaseModel):
    name: str | None
    last_name: str | None


class ProfileUpdate(ProfileBase):
    pass


class ProfileCreate(ProfileBase):
    user_id: int


class Profile(ProfileCreate):
    id: int
    avatar: Optional["Avatar"] = None


class AvatarBase(BaseModel):
    profile_id: int
    avatar: bytes | None


class Avatar(AvatarBase):
    id: int


# POST RELATED
class PostBase(BaseModel):
    title: str
    body: str


class PostUpdate(PostBase):
    pass


class PostCreate(PostBase):
    user_id: int


class Post(PostCreate):
    id: int
    comments: list["Comment"] = []


class PostNoComments(PostCreate):
    id: int


class CommentBase(BaseModel):
    body: str


class CommentUpdate(CommentBase):
    pass


class CommentCreate(CommentBase):
    post_id: int
    user_id: int


class Comment(CommentCreate):
    id: int
