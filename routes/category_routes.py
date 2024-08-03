from fastapi import APIRouter, HTTPException
from controllers.category_controller import add_category, get_categories
from validation.category_validation import CategoryCreate

router = APIRouter()

@router.post("/create")
async def create_category(category: CategoryCreate):
    return await add_category(category)

@router.get("/list")
async def list_categories():
    return await get_categories()