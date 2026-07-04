from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.core.enums import OrderStatus


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: OrderStatus
    created_at: datetime

    order_items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus