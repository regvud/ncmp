from fastapi import APIRouter, Depends

from db import db_dependency, delete_db_model, save_db_model, update_db_model
from models import Product
from permissions import owner_permission
from products.crud import get_product_by_id, get_product_list
from schemas import AuthenticatedUser, ProductBaseSchema, ProductSchema

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/create", response_model=ProductSchema)
async def product_create(
    db: db_dependency,
    product: ProductBaseSchema,
    current_user: AuthenticatedUser = Depends(owner_permission),
):
    new_product = Product(**product.model_dump())
    save_db_model(db, new_product)
    return new_product


@router.get("/", response_model=list[ProductSchema])
async def product_list(db: db_dependency):
    return get_product_list(db)


@router.get("/{product_id}", response_model=ProductSchema)
async def product_by_id(db: db_dependency, product_id: int):
    return get_product_by_id(db, product_id)


@router.put("/{product_id}", response_model=ProductSchema)
async def product_put(
    db: db_dependency, product_id: int, updated_product: ProductBaseSchema
):
    db_product = get_product_by_id(db, product_id)

    for k, v in updated_product:
        setattr(db_product, k, v)

    update_db_model(db, db_product)

    return db_product


@router.delete("/{product_id}")
async def product_delete(
    db: db_dependency,
    product_id: int,
    current_user: AuthenticatedUser = Depends(owner_permission),
):
    product_to_delete = get_product_by_id(db, product_id)
    delete_db_model(db, product_to_delete)
    return {"detail": f"Deleted product: {product_id}"}
