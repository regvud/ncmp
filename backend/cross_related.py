import os
from typing import Optional
from uuid import uuid1

from fastapi import UploadFile
from passlib.context import CryptContext

from enums import ImageTypeEnum
from exceptions import write_file_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
                    print(f"matched images {image_file}")
                    os.remove(f"{path}/{image_file}")

        case ImageTypeEnum.AVATAR:
            path = "images/avatars"
            for image_file in os.listdir(path):
                if image_file.startswith(str(prefix)):
                    print(f"matched avatars {image_file}")
                    os.remove(f"{path}/{image_file}")
