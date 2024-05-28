from sqlalchemy import (DECIMAL, Boolean, Column, DateTime, Enum, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db import Base
from enums import ContentTypeEnum, NotificationTypeEnum, ProductTypeEnum


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
    notifications = relationship(
        "Notification",
        uselist=True,
        backref="profiles",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="dynamic",
    )


class ProfileAvatar(BaseDataModel):
    __tablename__ = "profile_avatars"

    id = Column(Integer, primary_key=True)

    profile_id = Column(
        Integer, ForeignKey("profiles.id", ondelete="CASCADE"), index=True
    )
    avatar = Column(String)


class Notification(BaseDataModel):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)

    profile_id = Column(
        Integer, ForeignKey("profiles.id", ondelete="CASCADE"), index=True
    )
    type = Column(Enum(NotificationTypeEnum), index=True, nullable=False)
    message = Column(String(100))
    status = Column(Boolean, nullable=False, default=False)


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
    images = relationship(
        "PostImage",
        uselist=True,
        backref="posts",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def comments_count(self):
        return self.comments.count()


class PostImage(BaseDataModel):
    __tablename__ = "post_images"

    id = Column(Integer, primary_key=True)

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), index=True)
    path = Column(String)


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

    def replies_count(self):
        return self.replies.count()


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
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class UserLike(BaseDataModel):
    __tablename__ = "user_like"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    like_id = Column(Integer, ForeignKey("likes.id", ondelete="CASCADE"), index=True)


# PRODUCTS
class Product(BaseDataModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False, unique=True, index=True)
    type = Column(Enum(ProductTypeEnum), nullable=False, index=True)
    price = Column(DECIMAL(precision=7, scale=2), default=0, index=True)
    height = Column(Integer, nullable=True)
    width = Column(Integer, nullable=True)
    capacity = Column(DECIMAL(precision=3, scale=1), nullable=True)
    description = Column(String(255))
