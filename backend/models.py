from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base


class BaseDataModel(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# USER RELATED
class User(BaseDataModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String(50), index=True, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    is_owner = Column(Boolean, default=False)

    profile = relationship("Profile", uselist=False, backref="users")
    posts = relationship(
        "Post",
        uselist=True,
        backref="users",
        lazy="dynamic",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    comments = relationship(
        "Comment",
        uselist=True,
        backref="users",
        lazy="dynamic",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Profile(BaseDataModel):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    name = Column(String(25), index=True, nullable=True)
    last_name = Column(String(25), index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    avatar = relationship("ProfileAvatar", uselist=False, backref="profiles")


class ProfileAvatar(BaseDataModel):
    __tablename__ = "profile_avatars"

    id = Column(Integer, primary_key=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"), index=True)
    avatar = Column(LargeBinary)


# POST RELATED
class Post(BaseDataModel):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), index=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    comments = relationship(
        "Comment",
        uselist=True,
        backref="posts",
        lazy="dynamic",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Comment(BaseDataModel):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    body = Column(String(1000))
    post_id = Column(Integer, ForeignKey("posts.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    replies = relationship(
        "Reply",
        uselist=True,
        backref="comments",
        lazy="dynamic",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Reply(BaseDataModel):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True)

    body = Column(String(1000))
    comment_id = Column(Integer, ForeignKey("comments.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    to_user = Column(Integer, ForeignKey("users.id"), index=True)
