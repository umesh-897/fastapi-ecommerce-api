from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate,ProductUpdate
from sqlalchemy import asc, desc, or_
from fastapi import HTTPException


def create_product(db: Session, product: ProductCreate):

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        image_url=product.image_url,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product



def get_all_products(
    db: Session,
    page: int,
    limit: int,
    search: str | None,
    sort_by: str,
    sort_order: str,
    min_price: float | None,
    max_price: float | None,
    in_stock: bool | None,
):

    query = db.query(Product)

    # Validate sort order
    if sort_order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="sort_order must be asc or desc"
        )

    # Validate price range
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price"
        )

    # Search
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%")
            )
        )

    # Price Filter
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Stock Filter
    if in_stock:
        query = query.filter(Product.stock > 0)

    # Sorting
    
    ALLOWED_SORT_FIELDS = {
    "name": Product.name,
    "price": Product.price,
    "stock": Product.stock,
    "created_at": Product.created_at,
    }

    column = ALLOWED_SORT_FIELDS.get(sort_by)

    if column is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if sort_order.lower() == "desc":
        query = query.order_by(desc(column))
    else:
        query = query.order_by(asc(column))

    total = query.count()

    products = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return total, products

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
):

    product = get_product_by_id(db, product_id)

    if not product:
        return None

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock
    product.image_url = product_data.image_url
    product.is_available = product_data.is_available

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product_id: int
):

    product = get_product_by_id(
        db,
        product_id
    )

    if not product:
        return None

    db.delete(product)
    db.commit()

    return product