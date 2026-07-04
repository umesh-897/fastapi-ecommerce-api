from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str
    description: str | None = None


class CategoryResponse(CategoryCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)