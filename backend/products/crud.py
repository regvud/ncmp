from fastapi import HTTPException

from db import db_dependency
from models import Product


def get_product_by_id(db: db_dependency, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


def get_product_list(db: db_dependency):
    return db.query(Product).order_by(Product.id).all()
