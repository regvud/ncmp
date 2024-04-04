from typing import Optional

from pydantic import BaseModel


# USER RELATED
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    profile: "Profile"


class ProfileBase(BaseModel):
    name: str | None
    last_name: str | None
    user_id: int


class Profile(ProfileBase):
    id: int
    avatar: Optional["Avatar"] = None


class AvatarBase(BaseModel):
    profile_id: int
    avatar: bytes | None


class Avatar(AvatarBase):
    id: int
