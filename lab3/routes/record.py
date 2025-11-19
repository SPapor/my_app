from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database.service import get_db
from database import models
from schemas import record as schemas

router = APIRouter(prefix="/record", tags=["Record"])


@router.post("/", response_model=schemas.RecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(record_data: schemas.RecordCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == record_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    category = db.query(models.Category).filter(models.Category.id == record_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if not category.is_global and category.user_id != record_data.user_id:
        raise HTTPException(
            status_code=403,
            detail="У вас нема прав"
        )

    new_record = models.Record(**record_data.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/{record_id}", response_model=schemas.RecordResponse)
def get_record(record_id: UUID, db: Session = Depends(get_db)):
    record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.get("/", response_model=List[schemas.RecordResponse])
def get_records(
    user_id: Optional[UUID] = None,
    category_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    if user_id is None and category_id is None:
        raise HTTPException(status_code=400, detail="Provide user_id or category_id")

    query = db.query(models.Record)

    if user_id:
        query = query.filter(models.Record.user_id == user_id)

    if category_id:
        query = query.filter(models.Record.category_id == category_id)

    return query.all()


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: UUID, db: Session = Depends(get_db)):
    record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()
    return None