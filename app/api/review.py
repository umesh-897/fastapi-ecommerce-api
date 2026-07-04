from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ProductRatingResponse,
)
from app.services.review_service import (
    add_review,
    edit_review,
    remove_review,
    get_reviews,
    get_rating,
)

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post(
    "/",
    response_model=ReviewResponse,
)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_review(
        db,
        current_user,
        review,
    )


@router.get(
    "/product/{product_id}",
    response_model=list[ReviewResponse],
)
def get_product_reviews(
    product_id: int,
    db: Session = Depends(get_db),
):
    return get_reviews(
        db,
        product_id,
    )


@router.get(
    "/product/{product_id}/rating",
    response_model=ProductRatingResponse,
)
def get_product_rating(
    product_id: int,
    db: Session = Depends(get_db),
):
    return get_rating(
        db,
        product_id,
    )


@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
)
def update_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return edit_review(
        db,
        current_user,
        review_id,
        review,
    )


@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_review(
        db,
        current_user,
        review_id,
    )