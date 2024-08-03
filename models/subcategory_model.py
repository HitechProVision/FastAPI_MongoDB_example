from pydantic import BaseModel, Field
from datetime import datetime
from models.category_model import Category
from bson import ObjectId

class Subcategory(BaseModel):
    name: str
    category:str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True