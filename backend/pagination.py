from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.sql import select

from db import db_dependency


class Pagination:
    @staticmethod
    def paginator(db: db_dependency, model, page: int, size: int):
        params = Params(page=page, size=size)
        pag_res = paginate(db, select(model).order_by(model.created_at), params=params)
        return pag_res
