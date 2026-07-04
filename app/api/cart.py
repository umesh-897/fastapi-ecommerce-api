from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
    CartResponse,
)
from app.services.cart_service import (
    add_to_cart,
    get_cart,
    change_quantity,
    remove_from_cart,
    remove_all_cart_items,
)

router = APIRouter(
    prefix="/cart",
    tags=["Shopping Cart"],
)


@router.post("/", response_model=CartItemResponse)
def add_item_to_cart(
    cart_data: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_to_cart(
        db,
        current_user,
        cart_data,
    )


@router.get("/", response_model=CartResponse)
def get_my_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_cart(
        db,
        current_user,
    )


@router.put("/{cart_item_id}", response_model=CartItemResponse)
def update_cart_item(
    cart_item_id: int,
    cart_data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return change_quantity(
        db,
        current_user,
        cart_item_id,
        cart_data,
    )


@router.delete("/{cart_item_id}")
def delete_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_from_cart(
        db,
        current_user,
        cart_item_id,
    )


@router.delete("/")
def clear_my_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_all_cart_items(
        db,
        current_user,
    )