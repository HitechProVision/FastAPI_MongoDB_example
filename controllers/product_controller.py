from models.product_model import Product
from models.category_model import Category
from models.subcategory_model import Subcategory
from validation.product_validation import ProductCreate
from db import db
from fastapi import HTTPException
from bson import ObjectId


async def add_product(product: ProductCreate):
    product_obj = Product(**product.dict())
    result = db.products.insert_one(product_obj.dict())
    # product_obj.id = str(result.inserted_id)
    return product_obj

async def get_products():
    products = []
    for product in db.products.find():
        category_id = product.get("category")
        subcategory_id = product.get("subcategory")
        if category_id:
            category = db.categories.find_one({"_id": ObjectId(category_id)})
            if category:
                product["category"] = category["name"]
        
        if subcategory_id:
            subcategory = db.subcategories.find_one({"_id": ObjectId(subcategory_id)})
            if subcategory:
                product["subcategory"] = subcategory["name"]
        
        product["_id"] = str(product["_id"])
        products.append(product)
    return products


async def add_bulk_products(products_data: list[ProductCreate]):
    print(products_data)
    category_cache = {}
    subcategory_cache = {}

    # Check all categories and subcategories in the database
    for product in products_data:
        category_name = product.category
        subcategory_name = product.subcategory

        if category_name not in category_cache:
            category = db.categories.find_one({"name": category_name})
            if not category:
                raise HTTPException(status_code=400, detail=f"Category '{category_name}' not found in database.")
            category_cache[category_name] = str(category["_id"])

        if subcategory_name not in subcategory_cache:
            subcategory = db.subcategories.find_one({"name": subcategory_name})
            if not subcategory:
                raise HTTPException(status_code=400, detail=f"Subcategory '{subcategory_name}' not found in database.")
            subcategory_cache[subcategory_name] = str(subcategory["_id"])

    # Insert products if all categories and subcategories are valid
    product_objs = []
    for product in products_data:
        product_dict = product.dict()
        product_dict['category'] = category_cache[product.category]
        product_dict['subcategory'] = subcategory_cache[product.subcategory]
        product_objs.append(Product(**product_dict))

    result = db.products.insert_many([product.dict() for product in product_objs])
    for product, inserted_id in zip(product_objs, result.inserted_ids):
        product.id = str(inserted_id)
    return product_objs