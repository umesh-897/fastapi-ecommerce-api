from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.user import User
from app.repositories.review_repository import (
    get_review_by_user_and_product,
    create_review,
    update_review,
    delete_review,
    get_review_by_id,
    get_product_reviews,
    get_product_rating,
    has_purchased_product,
)
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
)


def add_review(
    db: Session,
    current_user: User,
    review_data: ReviewCreate,
):
    # Check if the user purchased the product
    if not has_purchased_product(
        db,
        current_user.id,
        review_data.product_id,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Purchase required before reviewing this product.",
        )

    # Check if review already exists
    existing_review = get_review_by_user_and_product(
        db,
        current_user.id,
        review_data.product_id,
    )

    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product.",
        )

    review = Review(
        user_id=current_user.id,
        product_id=review_data.product_id,
        rating=review_data.rating,
        comment=review_data.comment,
    )

    return create_review(
        db,
        review,
    )


def edit_review(
    db: Session,
    current_user: User,
    review_id: int,
    review_data: ReviewUpdate,
):
    review = get_review_by_id(
        db,
        review_id,
    )

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to edit this review.",
        )

    review.rating = review_data.rating
    review.comment = review_data.comment

    return update_review(
        db,
        review,
    )


def remove_review(
    db: Session,
    current_user: User,
    review_id: int,
):
    review = get_review_by_id(
        db,
        review_id,
    )

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found.",
        )

    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this review.",
        )

    delete_review(
        db,
        review,
    )

    return {
        "message": "Review deleted successfully."
    }


def get_reviews(
    db: Session,
    product_id: int,
):
    return get_product_reviews(
        db,
        product_id,
    )


def get_rating(
    db: Session,
    product_id: int,
):
    return get_product_rating(
        db,
        product_id,
    )