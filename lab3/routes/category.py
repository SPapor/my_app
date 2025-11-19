from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.service import get_db
from database import models
from schemas import category as schemas

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/", response_model=schemas.CategoryResponse)
def create_category(cat_data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    if not cat_data.is_global and cat_data.user_id:
        user = db.query(models.User).filter(models.User.id == cat_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    new_cat = models.Category(**cat_data.dict())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat




@router.get("/", response_model=List[schemas.CategoryResponse])
def get_categories(user_id: Optional[UUID] = None, db: Session = Depends(get_db)):
    query = db.query(models.Category).filter(models.Category.is_global == True)

    if user_id:
        private_query = db.query(models.Category).filter(
            models.Category.is_global == False,
            models.Category.user_id == user_id
        )
        return query.union(private_query).all()

    return query.all()


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: UUID, db: Session = Depends(get_db)):  # <--- int -> UUID
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return None