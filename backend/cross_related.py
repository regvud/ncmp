from uuid import uuid1

from fastapi import UploadFile
from passlib.context import CryptContext

from exceptions import write_file_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def uuid_creator(file_name: str):
    return f"{uuid1()}:{file_name.replace(' ', '').strip()}"


def write_image_file(upload_file: UploadFile, path_to_file: str) -> None:
    try:
        with open(path_to_file, "+wb") as file:
            file.write(upload_file.file.read())
    except Exception as e:
        raise write_file_exception(e)
