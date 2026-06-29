from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate,ProductUpdate


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

def get_all_products(db: Session):
    return db.query(Product).all()

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