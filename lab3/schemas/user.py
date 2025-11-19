from pydantic import BaseModel, Field
from uuid import UUID

class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: UUID
    class Config:
        from_attributes = True