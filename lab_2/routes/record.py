from fastapi import APIRouter, HTTPException, status, Query
import uuid
from datetime import datetime
from typing import Optional
from models.record import Record, RecordCreate
from storage.memory_storage import records, users, categories

router = APIRouter(prefix="/record", tags=["Record"])


@router.post("/", response_model=Record, status_code=status.HTTP_201_CREATED)
def create_record_route(record_data: RecordCreate):
    if record_data.user_id not in users:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    if record_data.category_id not in categories:
        raise HTTPException(status_code=404, detail="Категорію не знайдено")

    record_id = uuid.uuid4().hex
    date_time = datetime.now()

    record = {
        "id": record_id,
        "date_time": date_time,
        **record_data.model_dump()
    }
    records[record_id] = record
    return record


@router.get("/{record_id}", response_model=Record)
def get_record_route(record_id: str):
    if record_id not in records:
        raise HTTPException(status_code=404, detail="Запис не знайдено")
    return records[record_id]


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record_route(record_id: str):
    if record_id in records:
        del records[record_id]
        return
    raise HTTPException(status_code=404, detail="Запис не знайдено")


@router.get("/", response_model=list[Record], summary="Отримання списку записів з фільтрацією")
def get_records_filtered(
        user_id: Optional[str] = Query(None, description="ID користувача для фільтрації [cite: 31]"),
        category_id: Optional[str] = Query(None, description="ID категорії для фільтрації [cite: 31]")
):
    if user_id is None and category_id is None:
        raise HTTPException(
            status_code=400,
            detail="Потрібно надати принаймні user_id або category_id для фільтрації."
        )

    filtered_records = list(records.values())

    if user_id is not None:
        if user_id not in users:
            raise HTTPException(status_code=404, detail=f"Користувача з ID {user_id} не знайдено.")
        filtered_records = [r for r in filtered_records if r.get("user_id") == user_id]

    if category_id is not None:
        if category_id not in categories:
            raise HTTPException(status_code=404, detail=f"Категорію з ID {category_id} не знайдено.")
        filtered_records = [r for r in filtered_records if r.get("category_id") == category_id]

    return filtered_records