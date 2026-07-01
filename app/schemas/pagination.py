from pydantic import BaseModel
from typing import Generic, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    total: int
    page: int
    limit: int
    total_pages: int
    data: list[T]