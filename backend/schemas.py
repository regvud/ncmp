from datetime import datetime
from decimal import Decimal
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class CreatedUpdated(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class PaginatedSchema(BaseModel, Generic[T]):
    items: list[T] = []
    pages: int
    page: int
    size: int


class StatsLikes(BaseModel):
    likes_count: int


class UserIdAvatarSchema(BaseModel):
    userId: int
    avatar: str


# USER RELATED
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    is_owner: Optional[bool] = False


class User(UserBase, CreatedUpdated):
    id: int
    is_active: bool
    is_owner: bool
    profile: "Profile"
    posts: list["PostNoComments"] = []
    comments: list["Comment"] = []


# AUTH
class Tokens(BaseModel):
    access: str
    refresh: str


class SwaggerToken(BaseModel):
    access_token: str
    token_type: str


class RefreshTokenModel(BaseModel):
    refresh_token: str


# AUTH USER
class AuthenticatedUser(UserBase):
    id: int
    exp: float
    is_owner: bool
    is_active: bool


class UserAuthSchema(UserBase):
    password: str


class OauthUserSchema(BaseModel):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    at_hash: str
    nonce: str
    name: str
    picture: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    iat: int
    exp: int


# PROFILE
class ProfileBase(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None


class ProfileUpdate(ProfileBase):
    pass


class Profile(ProfileUpdate, CreatedUpdated):
    id: int

    user_id: int
    avatar: Optional["Avatar"] = None
    notifications: list["Notification"] = []


class AvatarBase(BaseModel):
    profile_id: int
    avatar: bytes


class AvatarCreate(AvatarBase):
    pass


class Avatar(AvatarBase, CreatedUpdated):
    id: int


class NotificationCreate(BaseModel):
    profile_id: int
    type: str
    message: str
    status: bool


class Notification(NotificationCreate, CreatedUpdated):
    id: int


# POST RELATED
class PostBase(BaseModel):
    title: str
    body: str


class PostUpdate(PostBase):
    pass


class PostCreate(PostBase):
    pass


class Post(PostCreate, CreatedUpdated):
    id: int

    user_id: int
    images: list["PostImageSchema"] = []
    comments: list["Comment"] = []
    likes: list["UserLike"] = []


class PostNoComments(PostCreate, CreatedUpdated):
    id: int

    user_id: int
    likes: list["UserLike"] = []


class PostCounterSchema(PostBase, StatsLikes):
    id: int

    user_id: int
    users_liked: list[UserIdAvatarSchema] = []

    images: list["PostImageSchema"] = []

    comments_count: int
    comments: list["CommentRepliesCounterSchema"] = []


class PostImageSchema(CreatedUpdated, BaseModel):
    id: int

    post_id: int
    path: str


# COMMENT
class CommentBase(BaseModel):
    body: str


class CommentUpdate(CommentBase):
    pass


class CommentCreate(CommentBase):
    pass


class Comment(CommentCreate, CreatedUpdated):
    id: int

    post_id: int
    user_id: int
    replies: list["Reply"] = []


class CommentRepliesCounterSchema(CommentBase, StatsLikes, CreatedUpdated):
    id: int

    post_id: int
    user_id: int
    replies: list["ReplyCounterSchema"] = []

    replies_count: int


# REPLIES
class ReplyBase(BaseModel):
    body: str


class ReplyUpdate(ReplyBase):
    pass


class ReplyCreate(ReplyBase):
    pass


class Reply(ReplyCreate, CreatedUpdated):
    id: int

    comment_id: int
    to_user: int
    user_id: int


class ReplyCounterSchema(Reply, StatsLikes):
    pass


# LIKES
class UserLikeCreate(BaseModel):
    user_id: int
    like_id: int


class UserLike(UserLikeCreate, CreatedUpdated):
    id: int


class LikeBase(BaseModel):
    content_id: int
    content_type: str


class Like(LikeBase, CreatedUpdated):
    id: int

    users_liked: list[UserLike] = []


class LikeCounter(LikeBase):
    id: int

    count: int
    users_liked: list[int] = []


# PRODUCTS
class ProductBaseSchema(BaseModel):
    name: str
    type: str
    price: Optional[Decimal] = None
    height: Optional[int] = None
    width: Optional[int] = None
    capacity: Optional[Decimal] = None
    description: Optional[str] = None


class ProductSchema(ProductBaseSchema, CreatedUpdated):
    id: int
