from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.user import User
from app.api.user import router as user_router
from app.models.product import Product
from app.api.product import router as product_router
from app.models.category import Category
from app.api.category import router as category_router
from app.models.cart import CartItem
from app.api.cart import router as cart_router
from app.models.order import Order
from app.models.order_item import OrderItem
from app.api.order import router as order_router
from app.models.review import Review
from app.api.review import router as review_router
from app.api.admin import router as admin_router
from app.core.exceptions import register_exception_handlers
from app.core.logging_config import setup_logging

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="E-Commerce API",
    description="Backend API for an E-Commerce application",
    version="1.0.0"
)

setup_logging()
register_exception_handlers(app)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(review_router)
app.include_router(admin_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the E-Commerce API"
    }

@app.get("/health")
def health_check():
    return {
        "status": "Running"
    }


@app.get("/db-check")

def db_check():
    with engine.connect() as connection:
        return {'message': "Database is connected successfully"}
    

