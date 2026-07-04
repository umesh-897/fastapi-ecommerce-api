from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False, index=True)

    description = Column(Text, nullable=True)

    price = Column(Float, nullable=False)

    stock = Column(Integer, default=0)

    image_url = Column(String(255), nullable=True)

    category_id = Column(
    Integer,
    ForeignKey("categories.id"),
    nullable=False,
    )

    is_available = Column(Boolean, default=True)


    category = relationship(
        "Category",
        back_populates="products"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cart_items = relationship(
        "CartItem",
        back_populates="product",
    )

    category = relationship(
        "Category",
        back_populates="products",
    )

    cart_items = relationship(
        "CartItem",
        back_populates="product",
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product",
    )


    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete-orphan",
    )






