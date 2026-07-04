from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import OrderStatus
from app.models.user import User
from app.repositories.cart_repository import (
    get_user_cart,
    clear_cart,
)
from app.repositories.order_repository import (
    create_order,
    create_order_item,
    get_orders_by_user,
    get_order_by_id,
    commit_transaction,
    rollback_transaction,
)


def checkout(
    db: Session,
    current_user: User,
):
    cart_items = get_user_cart(
        db,
        current_user.id,
    )

    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty",
        )

    total_amount = 0

    try:

        # Validate stock and calculate total
        for item in cart_items:

            if not item.product.is_available:
                raise HTTPException(
                    status_code=400,
                    detail=f"{item.product.name} is unavailable",
                )

            if item.quantity > item.product.stock:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for {item.product.name}",
                )

            total_amount += (
                item.quantity * item.product.price
            )

        # Create Order
        order = create_order(
            db,
            current_user.id,
            total_amount,
        )

        # Create Order Items
        for item in cart_items:

            create_order_item(
                db,
                order.id,
                item.product.id,
                item.quantity,
                item.product.price,
            )

            # Reduce stock
            item.product.stock -= item.quantity

        # Clear cart
        clear_cart(
            db,
            current_user.id,
        )

        commit_transaction(db)

        db.refresh(order)

        return order

    except Exception:
        rollback_transaction(db)
        raise


def get_my_orders(
    db: Session,
    current_user: User,
):
    return get_orders_by_user(
        db,
        current_user.id,
    )


def get_my_order(
    db: Session,
    current_user: User,
    order_id: int,
):
    order = get_order_by_id(
        db,
        order_id,
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )

    return order


def update_order_status(
    db: Session,
    order_id: int,
    status: OrderStatus,
):
    order = get_order_by_id(
        db,
        order_id,
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    order.status = status

    commit_transaction(db)

    db.refresh(order)

    return order