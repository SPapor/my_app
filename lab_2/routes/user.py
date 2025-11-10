from fastapi import APIRouter, HTTPException, status
import uuid
from models.user import User, UserCreate
from storage.memory_storage import users, records

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_route(user_data: UserCreate):
    user_id = uuid.uuid4().hex
    user = {"id": user_id, **user_data.model_dump()}
    users[user_id] = user
    return user

@router.get("s", response_model=list[User])
def get_all_users_route():
    return list(users.values())

@router.get("/{user_id}", response_model=User)
def get_user_route(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return users[user_id]

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(user_id: str):
    if user_id in users:
        del users[user_id]
        records_to_delete = [rid for rid, r in records.items() if r.get("user_id") == user_id]
        for rid in records_to_delete:
            del records[rid]
        return
    raise HTTPException(status_code=404, detail="Користувача не знайдено")