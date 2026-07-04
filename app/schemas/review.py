from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(
        ge=1,
        le=5,
        description="Rating must be between 1 and 5",
    )
    comment: str | None = None


class ReviewUpdate(BaseModel):
    rating: int = Field(
        ge=1,
        le=5,
        description="Rating must be between 1 and 5",
    )
    comment: str | None = None


class ReviewUser(BaseModel):
    id: int
    full_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class ReviewResponse(BaseModel):
    id: int
    rating: int
    comment: str | None
    created_at: datetime

    user: ReviewUser

    model_config = ConfigDict(
        from_attributes=True
    )


class ProductRatingResponse(BaseModel):
    average_rating: float
    total_reviews: int