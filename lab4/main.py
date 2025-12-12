from fastapi import FastAPI
from routes import user, category, record, auth

app = FastAPI()

app.include_router(user.router)
app.include_router(category.router)
app.include_router(record.router)
app.include_router(auth.router)