# main.py
from fastapi import FastAPI
from routes import user, category, record

app = FastAPI(
    title="Лабораторна 2: Розробка базового REST API",
    description="Базовий REST API для обліку витрат [cite: 3]",
    version="1.0.0"
)

app.include_router(user.router)
app.include_router(category.router)
app.include_router(record.router)

