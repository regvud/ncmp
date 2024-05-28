import os
from os import environ as env
from typing import Optional
from uuid import uuid1

from dotenv import load_dotenv
from fastapi import UploadFile
from passlib.context import CryptContext
from sqlalchemy import Table

from db import Base, db_dependency
from enums import ContentTypeEnum, ImageTypeEnum
from exceptions import write_file_exception

load_dotenv()


pwd_context = CryptContext(schemes=[env.get("PWD_SCHEMA")], deprecated="auto")


def uuid_creator(file_name: str, prefix: Optional[str]):
    return f"{prefix}-{uuid1()}:{file_name.replace(' ', '').strip()}"


def write_image_file(upload_file: UploadFile, path_to_file: str) -> None:
    try:
        with open(path_to_file, "+wb") as file:
            file.write(upload_file.file.read())
    except Exception as e:
        raise write_file_exception(e)


def delete_related_images(image_type: ImageTypeEnum, prefix: int):
    match image_type:
        case ImageTypeEnum.POST:
            path = "images/posts"
            for image_file in os.listdir(path):
                if image_file.startswith(str(prefix)):
                    os.remove(f"{path}/{image_file}")

        case ImageTypeEnum.AVATAR:
            path = "images/avatars"
            for image_file in os.listdir(path):
                if image_file.startswith(str(prefix)):
                    os.remove(f"{path}/{image_file}")


def delete_related_db_models(
    db: db_dependency, content_id: int, content_type: ContentTypeEnum
):
    like_table = Table("likes", Base.metadata, autoload=True)
    q = (
        db.query(like_table)
        .filter(like_table.c.content_id == content_id)
        .filter(like_table.c.content_type == content_type)
    )
    q.delete()
    db.commit()
