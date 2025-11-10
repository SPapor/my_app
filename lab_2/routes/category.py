from fastapi import APIRouter, HTTPException, status
import uuid
from models.category import Category, CategoryCreate
from storage.memory_storage import categories, records

router = APIRouter(prefix="/category", tags=["Category"])

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category_route(category_data: CategoryCreate):
    category_id = uuid.uuid4().hex
    category = {"id": category_id, **category_data.model_dump()}
    categories[category_id] = category
    return category

@router.get("/", response_model=list[Category])
def get_all_categories_route():
    return list(categories.values())

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_route(category_id: str):
    if category_id in categories:
        del categories[category_id]
        records_to_delete = [rid for rid, r in records.items() if r.get("category_id") == category_id]
        for rid in records_to_delete:
            del records[rid]
        return
    raise HTTPException(status_code=404, detail="Категорію не знайдено")