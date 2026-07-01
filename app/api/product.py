from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse,ProductUpdate
from app.services.product_service import (add_product,
                                          list_products,
                                          get_product,
                                          edit_product,
                                          remove_product,
                                          )
from app.schemas.pagination import PaginatedResponse
from typing import Annotated
from app.schemas.pagination import PaginatedResponse


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    return add_product(db, product)


from app.schemas.pagination import PaginatedResponse


@router.get("/", response_model=PaginatedResponse[ProductResponse])
def get_products(

    page: Annotated[int, Query(ge=1)] = 1,

    limit: Annotated[int, Query(ge=1, le=100)] = 10,

    search: str | None = None,

    sort_by: str = "created_at",

    sort_order: str = "desc",

    min_price: float | None = None,

    max_price: float | None = None,

    in_stock: bool | None = None,

    db: Session = Depends(get_db),
):

    return list_products(
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



@router.get("/{product_id}", response_model=ProductResponse)
def get_single_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    return get_product(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_api(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    return edit_product(
        db,
        product_id,
        product
    )


@router.delete("/{product_id}")
def delete_product_api(
    product_id: int,
    db: Session = Depends(get_db),
):
    remove_product(db, product_id)

    return {
        "message": "Product deleted successfully"
    }