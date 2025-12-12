from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.service import get_db
from database import models
from schemas import user as schemas
from utils.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])




@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
        user_id: UUID,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("s", response_model=List[schemas.UserResponse])
def get_all_users(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    return db.query(models.User).all()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: UUID,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return None