from fastapi import HTTPException, status

TOKEN_EXPIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is expired",
    headers={"WWW-Authenticate": "Bearer"},
)

UNAUTHORIZED_EXCEPTION = HTTPException(status_code=403, detail="Unauthorized user")
NOT_OWNER_EXCEPTION = HTTPException(status_code=403, detail="User is not owner")
