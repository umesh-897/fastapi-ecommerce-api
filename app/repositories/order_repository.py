from sqlalchemy.orm import Session, joinedload

from app.models.order import Order
from app.models.order_item import OrderItem


def create_order(
    db: Session,
    user_id: int,
    total_amount: float,
):
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="PENDING",
    )

    db.add(order)
    db.flush()

    return order


def create_order_item(
    db: Session,
    order_id: int,
    product_id: int,
    quantity: int,
    price: float,
):
    item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price,
    )

    db.add(item)


def get_orders_by_user(
    db: Session,
    user_id: int,
):
    return (
        db.query(Order)
        .options(joinedload(Order.order_items))
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order_by_id(
    db: Session,
    order_id: int,
):
    return (
        db.query(Order)
        .options(joinedload(Order.order_items))
        .filter(Order.id == order_id)
        .first()
    )


def commit_transaction(db: Session):
    db.commit()


def rollback_transaction(db: Session):
    db.rollback()