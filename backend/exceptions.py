from fastapi import HTTPException, status

TOKEN_EXPIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is expired",
    headers={"WWW-Authenticate": "Bearer"},
)

UNAUTHORIZED_EXCEPTION = HTTPException(status_code=403, detail="Unauthorized user")


def not_owner_exception(content_type: str):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"User is not owner of this {content_type}",
    )
