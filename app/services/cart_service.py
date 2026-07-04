from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.cart_repository import (
    get_cart_item,
    create_cart_item,
    get_user_cart,
    update_cart_item,
    delete_cart_item,
    clear_cart,
)
from app.repositories.product_repository import get_product_by_id
from app.schemas.cart import (
    CartItemCreate,
    CartItemUpdate,
    CartResponse,
)


def add_to_cart(
    db: Session,
    current_user: User,
    cart_data: CartItemCreate,
):

    product = get_product_by_id(
        db,
        cart_data.product_id,
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if not product.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not available",
        )

    if cart_data.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero",
        )

    if cart_data.quantity > product.stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested quantity exceeds available stock",
        )

    existing_item = get_cart_item(
        db,
        current_user.id,
        product.id,
    )

    if existing_item:

        new_quantity = existing_item.quantity + cart_data.quantity

        if new_quantity > product.stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requested quantity exceeds available stock",
            )

        existing_item.quantity = new_quantity

        return update_cart_item(
            db,
            existing_item,
        )

    return create_cart_item(
        db,
        current_user.id,
        product.id,
        cart_data.quantity,
    )


def get_cart(
    db: Session,
    current_user: User,
):

    items = get_user_cart(
        db,
        current_user.id,
    )

    total_items = 0
    total_amount = 0.0

    for item in items:
        total_items += item.quantity
        total_amount += item.quantity * item.product.price

    return CartResponse(
        items=items,
        total_items=total_items,
        total_amount=total_amount,
    )


def change_quantity(
    db: Session,
    current_user: User,
    cart_item_id: int,
    cart_data: CartItemUpdate,
):

    items = get_user_cart(
        db,
        current_user.id,
    )

    cart_item = next(
        (
            item
            for item in items
            if item.id == cart_item_id
        ),
        None,
    )

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found",
        )

    if cart_data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero",
        )

    if cart_data.quantity > cart_item.product.stock:
        raise HTTPException(
            status_code=400,
            detail="Requested quantity exceeds available stock",
        )

    cart_item.quantity = cart_data.quantity

    return update_cart_item(
        db,
        cart_item,
    )


def remove_from_cart(
    db: Session,
    current_user: User,
    cart_item_id: int,
):

    items = get_user_cart(
        db,
        current_user.id,
    )

    cart_item = next(
        (
            item
            for item in items
            if item.id == cart_item_id
        ),
        None,
    )

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found",
        )

    delete_cart_item(
        db,
        cart_item,
    )

    return {
        "message": "Item removed from cart"
    }


def remove_all_cart_items(
    db: Session,
    current_user: User,
):

    clear_cart(
        db,
        current_user.id,
    )

    return {
        "message": "Cart cleared successfully"
    }