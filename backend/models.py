from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base
from enums import ContentTypeEnum


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

    profile = relationship(
        "Profile",
        uselist=False,
        backref="users",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    avatar = relationship(
        "ProfileAvatar",
        uselist=False,
        backref="profiles",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ProfileAvatar(BaseDataModel):
    __tablename__ = "profile_avatars"

    id = Column(Integer, primary_key=True)

    profile_id = Column(
        Integer, ForeignKey("profiles.id", ondelete="CASCADE"), index=True
    )
    avatar = Column(LargeBinary)


# POST RELATED
class Post(BaseDataModel):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), index=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
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
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)

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
    comment_id = Column(
        Integer, ForeignKey("comments.id", ondelete="CASCADE"), index=True
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    to_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)


class Like(BaseDataModel):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)

    content_id = Column(Integer, index=True, nullable=False)
    content_type = Column(
        Enum(ContentTypeEnum), index=True, nullable=False
    )  # 'post', 'comment', or 'reply'

    users_liked = relationship(
        "UserLike",
        uselist=True,
        backref="likes",
        lazy="dynamic",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (CheckConstraint("count >= 0", name="min_count_constraint"),)


class UserLike(BaseDataModel):
    __tablename__ = "user_like"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    like_id = Column(Integer, ForeignKey("likes.id", ondelete="CASCADE"), index=True)
