from fastapi import FastAPI
from app.api.v1.api import api_router 

app = FastAPI(title="Ecommerce API v1")


app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"status": "Online"}