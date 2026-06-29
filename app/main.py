from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.user import User
from app.api.user import router as user_router
from app.models.product import Product
from app.api.product import router as product_router



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="E-Commerce API",
    description="Backend API for an E-Commerce application",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(product_router)



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