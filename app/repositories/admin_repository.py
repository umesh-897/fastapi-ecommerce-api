from sqlalchemy import func, extract
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem


def get_dashboard_summary(db: Session):
    total_users = db.query(func.count(User.id)).scalar()

    total_products = db.query(func.count(Product.id)).scalar()

    total_categories = db.query(func.count(Category.id)).scalar()

    total_orders = db.query(func.count(Order.id)).scalar()

    total_revenue = (
        db.query(func.sum(Order.total_amount))
        .scalar()
        or 0
    )

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_categories": total_categories,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
    }


def get_top_products(
    db: Session,
    limit: int = 5,
):
    results = (
        db.query(
            Product.name.label("product_name"),
            func.sum(OrderItem.quantity).label("units_sold"),
        )
        .join(OrderItem)
        .group_by(Product.id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(limit)
        .all()
    )

    return results


def get_top_categories(
    db: Session,
    limit: int = 5,
):
    results = (
        db.query(
            Category.name.label("category_name"),
            func.sum(OrderItem.quantity).label("units_sold"),
        )
        .select_from(Category)
        .join(
            Product,
            Product.category_id == Category.id,
        )
        .join(
            OrderItem,
            OrderItem.product_id == Product.id,
        )
        .group_by(
            Category.id,
            Category.name,
        )
        .order_by(
            func.sum(OrderItem.quantity).desc()
        )
        .limit(limit)
        .all()
    )

    return results


def get_monthly_sales(db: Session):
    results = (
        db.query(
            extract("month", Order.created_at).label("month"),
            func.sum(Order.total_amount).label("revenue"),
        )
        .group_by(extract("month", Order.created_at))
        .order_by(extract("month", Order.created_at))
        .all()
    )

    return results


def get_low_stock_products(
    db: Session,
    threshold: int = 5,
):
    return (
        db.query(Product)
        .filter(Product.stock <= threshold)
        .order_by(Product.stock.asc())
        .all()
    )