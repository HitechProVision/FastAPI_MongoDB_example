from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    name: str = Field(max_length=20)
    category: str
    subcategory: Optional[str] = None

