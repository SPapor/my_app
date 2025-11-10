from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

class User(UserCreate):
    id: str