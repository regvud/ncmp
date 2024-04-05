from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from backend.db import Base


# USER RELATED
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    email = Column(String, index=True, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    is_owner = Column(Boolean, default=False)

    profile = relationship("Profile", uselist=False, backref="users")
    posts = relationship("Post", uselist=True, backref="users")
    comments = relationship("Comment", uselist=True, backref="users")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    name = Column(String(25), index=True, nullable=True)
    last_name = Column(String(25), index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    avatar = relationship("ProfileAvatar", uselist=False, backref="profiles")


class ProfileAvatar(Base):
    __tablename__ = "profile_avatars"

    id = Column(Integer, primary_key=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"), index=True)
    avatar = Column(LargeBinary)


# POST RELATED
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    title = Column(String, index=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    comments = relationship("Comment", uselist=True, backref="posts")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    body = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
