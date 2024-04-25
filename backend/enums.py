from enum import Enum


class ContentTypeEnum(Enum):
    POST = "post"
    COMMENT = "comment"
    REPLY = "reply"


class NotificationTypeEnum(Enum):
    LIKE = "like"
    REPLY = "reply"
    COMMENT = "comment"


class ImageTypeEnum(Enum):
    POST = "post"
    AVATAR = "avatar"


class ProductTypeEnum(Enum):
    PAN = "pan"  # каструля
    SKILLET = "skillet"  # сковорідка
    LID = "lid"  # кришка
    ELEC = "elec"
    OTHER = "other"
