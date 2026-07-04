from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship 



from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    phone = Column(String(15), nullable=True)

    is_active = Column(Boolean, default=True,nullable=False,)

    is_admin = Column(Boolean, default=False,nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cart_items = relationship(
        "CartItem",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    cart_items = relationship(
        "CartItem",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan",
    )