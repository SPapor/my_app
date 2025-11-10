from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str

class Category(CategoryCreate):
    id: str