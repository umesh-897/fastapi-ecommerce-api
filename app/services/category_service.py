from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.category_repository import (
    create_category,
    get_all_categories,
    get_category_by_id,
    get_category_by_name,
    update_category,
    delete_category,
)
from app.schemas.category import CategoryCreate,CategoryUpdate


def add_category(
    db: Session,
    category: CategoryCreate
):

    existing = db.query(get_category_by_id.__globals__["Category"]).filter_by(
    name=category.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    return create_category(db, category)


def list_categories(db: Session):

    return get_all_categories(db)


def get_category(
    db: Session,
    category_id: int
):

    category = get_category_by_id(
        db,
        category_id
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


def edit_category(
    db: Session,
    category_id: int,
    category: CategoryUpdate
):
    updated = update_category(
        db,
        category_id,
        category
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return updated


def remove_category(
    db: Session,
    category_id: int
):
    deleted = delete_category(
        db,
        category_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return deleted