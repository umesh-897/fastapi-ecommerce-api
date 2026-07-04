from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import admin_required
from app.core.database import get_db
from app.models.user import User
from app.schemas.admin import (
    DashboardResponse,
    TopProductResponse,
    TopCategoryResponse,
    MonthlySalesResponse,
    LowStockResponse,
)
from app.services.admin_service import (
    dashboard_summary,
    top_products,
    top_categories,
    monthly_sales,
    low_stock_products,
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get(
    "/dashboard",
    response_model=DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    return dashboard_summary(db)


@router.get(
    "/top-products",
    response_model=list[TopProductResponse],
)
def get_top_products(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    return top_products(
        db,
        limit,
    )


@router.get(
    "/top-categories",
    response_model=list[TopCategoryResponse],
)
def get_top_categories(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    return top_categories(
        db,
        limit,
    )


@router.get(
    "/monthly-sales",
    response_model=list[MonthlySalesResponse],
)
def get_sales(
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    return monthly_sales(db)


@router.get(
    "/low-stock",
    response_model=list[LowStockResponse],
)
def get_low_stock(
    threshold: int = Query(5, ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    return low_stock_products(
        db,
        threshold,
    )