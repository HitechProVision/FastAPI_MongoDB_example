from fastapi import APIRouter
from routes import category_routes, product_routes, subcategory_routes

router = APIRouter()

router.include_router(category_routes.router, prefix="/categories", tags=["categories"])
router.include_router(product_routes.router, prefix="/products", tags=["products"])
router.include_router(subcategory_routes.router, prefix="/subcategories", tags=["subcategories"])
