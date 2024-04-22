from fastapi import APIRouter, Depends

from content.crud import get_user_notifications, read_notifications
from db import db_dependency
from permissions import authenticated_permission
from schemas import AuthenticatedUser, Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=list[Notification])
async def view_notifications(
    db: db_dependency,
    current_user: AuthenticatedUser = Depends(authenticated_permission),
):
    return get_user_notifications(db, current_user.id)


@router.get("/read")
async def auth_user_read_notifications(
    db: db_dependency,
    current_user: AuthenticatedUser = Depends(authenticated_permission),
):
    readed_status = read_notifications(db, current_user.id)

    return {
        "detail": f"readed notifications of user {current_user.email}"
        if readed_status
        else "no unreaded notifications"
    }
