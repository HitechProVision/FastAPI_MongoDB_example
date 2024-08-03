from models.subcategory_model import Subcategory
from validation.subcategory_validation import SubcategoryCreate
from db import db
from bson import ObjectId


async def add_subcategory(subcategory: SubcategoryCreate):
    subcategory_obj = Subcategory(**subcategory.dict())
    result = db.subcategories.insert_one(subcategory_obj.dict())
    subcategory_obj._id = str(result.inserted_id)
    return subcategory_obj


async def get_subcategories():
    subCategories = []
    for subCategory in db.subcategories.find():
        category_id = subCategory.get("category")
        if category_id:
            print(category_id)
            category = db.categories.find_one({"_id": ObjectId(category_id)})
            if category:
                subCategory["category"] = category["name"]
        subCategory["_id"] = str(subCategory["_id"])
        subCategories.append(subCategory)
    return subCategories