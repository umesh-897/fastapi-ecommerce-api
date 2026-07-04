from sqlalchemy.orm import Session

from app.repositories.admin_repository import (
    get_dashboard_summary,
    get_top_products,
    get_top_categories,
    get_monthly_sales,
    get_low_stock_products,
)


def dashboard_summary(db: Session):
    return get_dashboard_summary(db)


def top_products(
    db: Session,
    limit: int = 5,
):
    return get_top_products(
        db,
        limit,
    )


def top_categories(
    db: Session,
    limit: int = 5,
):
    return get_top_categories(
        db,
        limit,
    )


def monthly_sales(db: Session):
    sales = get_monthly_sales(db)

    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    return [
        {
            "month": month_names.get(
                int(item.month),
                str(item.month),
            ),
            "revenue": item.revenue,
        }
        for item in sales
    ]


def low_stock_products(
    db: Session,
    threshold: int = 5,
):
    return get_low_stock_products(
        db,
        threshold,
    )