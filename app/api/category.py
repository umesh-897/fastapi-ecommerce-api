from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.admin import admin_required
from app.core.database import get_db
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category_service import (
    add_category,
    get_category,
    list_categories,
    edit_category,
    remove_category,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post("/", response_model=CategoryResponse)
def create_category_api(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return add_category(db, category)


@router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
):
    return list_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_single_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    return get_category(
        db,
        category_id,
    )


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_api(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return edit_category(
        db,
        category_id,
        category,
    )


@router.delete("/{category_id}")
def delete_category_api(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    remove_category(
        db,
        category_id,
    )

    return {
        "message": "Category deleted successfully"
    }