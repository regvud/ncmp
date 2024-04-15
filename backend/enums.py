from enum import Enum


class ContentTypeEnum(Enum):
    POST = "post"
    COMMENT = "comment"
    REPLY = "reply"


class NotificationTypeEnum(Enum):
    LIKE = "like"
    REPLY = "reply"
    COMMENT = "comment"
