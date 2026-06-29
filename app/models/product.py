from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
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

    is_available = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())