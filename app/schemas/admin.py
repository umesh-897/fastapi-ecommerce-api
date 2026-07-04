from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_users: int
    total_products: int
    total_categories: int
    total_orders: int
    total_revenue: float


class TopProductResponse(BaseModel):
    product_name: str
    units_sold: int


class TopCategoryResponse(BaseModel):
    category_name: str
    units_sold: int


class MonthlySalesResponse(BaseModel):
    month: str
    revenue: float


class LowStockResponse(BaseModel):
    id: int
    name: str
    stock: int