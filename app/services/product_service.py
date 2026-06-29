from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.schemas.product import ProductCreate,ProductUpdate

from app.repositories.product_repository import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
)

def add_product(db: Session, product: ProductCreate):
    return create_product(db, product)



def list_products(db: Session):
    return get_all_products(db)


def get_product(db: Session, product_id: int):

    product = get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


def edit_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
):

    product = update_product(
        db,
        product_id,
        product_data
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

def remove_product(
    db: Session,
    product_id: int
):

    product = delete_product(
        db,
        product_id
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product