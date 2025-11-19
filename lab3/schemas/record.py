from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class RecordBase(BaseModel):
    user_id: UUID
    category_id: UUID
    amount: float = Field(gt=0)

class RecordCreate(RecordBase):
    pass

class RecordResponse(RecordBase):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True