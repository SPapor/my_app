from fastapi import FastAPI
from lab_1.views import router

app = FastAPI()

app.include_router(router)
