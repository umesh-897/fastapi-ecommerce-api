from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.review import Review
from app.models.order import Order
from app.models.order_item import OrderItem


def get_review_by_user_and_product(
    db: Session,
    user_id: int,
    product_id: int,
):
    return (
        db.query(Review)
        .filter(
            Review.user_id == user_id,
            Review.product_id == product_id,
        )
        .first()
    )


def create_review(
    db: Session,
    review: Review,
):
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def update_review(
    db: Session,
    review: Review,
):
    db.commit()
    db.refresh(review)
    return review


def delete_review(
    db: Session,
    review: Review,
):
    db.delete(review)
    db.commit()


def get_review_by_id(
    db: Session,
    review_id: int,
):
    return (
        db.query(Review)
        .options(joinedload(Review.user))
        .filter(Review.id == review_id)
        .first()
    )


def get_product_reviews(
    db: Session,
    product_id: int,
):
    return (
        db.query(Review)
        .options(joinedload(Review.user))
        .filter(
            Review.product_id == product_id
        )
        .order_by(
            Review.created_at.desc()
        )
        .all()
    )


def get_product_rating(
    db: Session,
    product_id: int,
):
    average, total = (
        db.query(
            func.avg(Review.rating),
            func.count(Review.id),
        )
        .filter(
            Review.product_id == product_id
        )
        .first()
    )

    return {
        "average_rating": round(
            average or 0,
            2,
        ),
        "total_reviews": total,
    }


def has_purchased_product(
    db: Session,
    user_id: int,
    product_id: int,
):
    order = (
        db.query(Order)
        .join(OrderItem)
        .filter(
            Order.user_id == user_id,
            OrderItem.product_id == product_id,
        )
        .first()
    )

    return order is not None