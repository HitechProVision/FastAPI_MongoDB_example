from models.category_model import Category
from validation.category_validation import CategoryCreate
from db import db


async def add_category(category: CategoryCreate):
    category_obj = Category(**category.dict())
    result = db.categories.insert_one(category_obj.dict())
    return category_obj


async def get_categories():
    categories = []
    for category in db.categories.find():
        category["_id"] = str(category["_id"])
        categories.append(category)
    return categories
