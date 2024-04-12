from fastapi import HTTPException, status

from enums import ContentTypeEnum

TOKEN_EXPIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is expired",
    headers={"WWW-Authenticate": "Bearer"},
)
UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized user"
)


def liked_exception(content_type: ContentTypeEnum):
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"User already liked this {content_type.value}",
    )


def unliked_exception(content_type: ContentTypeEnum):
    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail=f"User already unliked this {content_type.value}",
    )


def not_owner_exception(content_type: ContentTypeEnum):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"User is not owner of this {content_type.value}",
    )
