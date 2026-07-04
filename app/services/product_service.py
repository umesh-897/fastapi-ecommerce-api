from sqlalchemy.orm import Session
from fastapi import HTTPException
from math import ceil

from app.schemas.product import ProductCreate,ProductUpdate
from app.repositories.category_repository import get_category_by_id
from app.repositories.product_repository import (
    create_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product,
)

def add_product(
    db: Session,
    product: ProductCreate,
):

    category = get_category_by_id(
        db,
        product.category_id,
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return create_product(
        db,
        product,
    )

def list_products(
    db,
    page,
    limit,
    search,
    sort_by,
    sort_order,
    min_price,
    max_price,
    in_stock,
):

    total, products = get_all_products(
        db,
        page,
        limit,
        search,
        sort_by,
        sort_order,
        min_price,
        max_price,
        in_stock,
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": ceil(total / limit) if total else 0,
        "data": products,
    }


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