from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(..., max_length=20)
    category: str
    subcategory: str= None
