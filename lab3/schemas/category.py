from pydantic import BaseModel, Field, model_validator
from typing import Optional
from uuid import UUID

class CategoryBase(BaseModel):
    name: str
    is_global: bool = True
    user_id: Optional[UUID] = None

class CategoryCreate(CategoryBase):
    @model_validator(mode='after')
    def check_category_logic(self):
        if self.is_global:
            self.user_id = None
        else:
            if self.user_id is None:
                raise ValueError("Для приватної категорії потрібен user_id")
        return self

class CategoryResponse(CategoryBase):
    id: UUID
    class Config:
        from_attributes = True