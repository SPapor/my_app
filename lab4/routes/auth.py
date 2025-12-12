from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from database.service import get_db
from database import models
from schemas import user as user_schemas
from utils.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=user_schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Створює нового користувача з хешуванням пароля."""
    if db.query(models.User).filter(models.User.name == user_data.name).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name already registered")

    hashed_password = get_password_hash(user_data.password)

    new_user = models.User(name=user_data.name, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login_for_access_token(user_data: user_schemas.UserLogin, db: Session = Depends(get_db)):
    """Логін користувача, повертає JWT токен."""
    user = db.query(models.User).filter(models.User.name == user_data.name).first()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}