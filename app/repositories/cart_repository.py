from sqlalchemy.orm import Session, joinedload

from app.models.cart import CartItem


def get_cart_item(
    db: Session,
    user_id: int,
    product_id: int,
):
    return (
        db.query(CartItem)
        .filter(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id,
        )
        .first()
    )


def create_cart_item(
    db: Session,
    user_id: int,
    product_id: int,
    quantity: int,
):
    item = CartItem(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def get_user_cart(
    db: Session,
    user_id: int,
):
    return (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == user_id)
        .all()
    )


def update_cart_item(
    db: Session,
    item: CartItem,
):
    db.commit()
    db.refresh(item)
    return item


def delete_cart_item(
    db: Session,
    item: CartItem,
):
    db.delete(item)
    db.commit()


def clear_cart(
    db: Session,
    user_id: int,
):
    db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).delete()

    db.commit()