from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class ProductInCart(BaseModel):
    id: int
    name: str
    price: float
    image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CartItemResponse(BaseModel):
    id: int
    quantity: int
    created_at: datetime

    product: ProductInCart

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total_items: int
    total_amount: float