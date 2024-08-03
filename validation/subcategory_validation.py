from pydantic import BaseModel, Field

class SubcategoryCreate(BaseModel):
    category: str
    name: str = Field(..., max_length=10)
