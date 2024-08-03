from fastapi import APIRouter, HTTPException
from controllers.subcategory_controller import add_subcategory, get_subcategories
from validation.subcategory_validation import SubcategoryCreate

router = APIRouter()

@router.post("/create")
async def create_subcategory(subcategory: SubcategoryCreate):
    return await add_subcategory(subcategory)


@router.get("/list")
async def list_subcategories():
    return await get_subcategories()