from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, admin_required
from app.core.database import get_db
from app.models.user import User
from app.schemas.order import (
    OrderResponse,
    OrderStatusUpdate,
)
from app.services.order_service import (
    checkout,
    get_my_orders,
    get_my_order,
    update_order_status,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "/checkout",
    response_model=OrderResponse,
)
def checkout_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return checkout(
        db,
        current_user,
    )


@router.get(
    "/",
    response_model=list[OrderResponse],
)
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_orders(
        db,
        current_user,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_order(
        db,
        current_user,
        order_id,
    )


@router.put(
    "/{order_id}/status",
    response_model=OrderResponse,
)
def change_order_status(
    order_id: int,
    order_status: OrderStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    return update_order_status(
        db,
        order_id,
        order_status.status,
    )