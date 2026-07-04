from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    image_url: str | None = None
    category_id: int


class ProductResponse(ProductCreate):
    id: int
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class ProductUpdate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    image_url: str | None = None
    category_id: int
    is_available: bool