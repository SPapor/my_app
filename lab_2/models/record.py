from pydantic import BaseModel
from datetime import datetime

class RecordCreate(BaseModel):
    user_id: str
    category_id: str
    amount: float

class Record(RecordCreate):
    id: str
    date_time: datetime 