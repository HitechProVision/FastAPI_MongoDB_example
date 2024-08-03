from fastapi import APIRouter, UploadFile, File, HTTPException
from controllers.product_controller import add_product, get_products, add_bulk_products
from validation.product_validation import ProductCreate
import pandas as pd

router = APIRouter()

@router.post("/create")
async def create_product(product: ProductCreate):
    return await add_product(product)

@router.get("/list")
async def list_products():
    return await get_products()

@router.post("/import")
async def import_products(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)
        products_data = []
        errors = []
        for index, row in df.iterrows():
            try:
                # print(row)

                # Validate and handle missing or invalid data
                if pd.isna(row['Product Name']) or pd.isna(row['Category']):
                    raise ValueError(f"Product Name, Category, and Subcategory must all be provided and valid strings.")
                
                product_data = ProductCreate(
                    name=str(row['Product Name']),
                    category=str(row['Category']),
                    subcategory=str(row['Subcategory'])
                )
                products_data.append(product_data)
            except Exception as e:
                errors.append(str(e))

        if errors:
            raise HTTPException(status_code=400, detail={"errors": errors})

        products = await add_bulk_products(products_data)
        return {"status": "success", "imported_products": [product.dict() for product in products]}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error importing products: {e}")