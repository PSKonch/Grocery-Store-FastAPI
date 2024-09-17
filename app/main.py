from fastapi import FastAPI
from app.backend.db import Base, engine
from app.routers import category, products, auth

app = FastAPI()

@app.get('/')
async def welcome() -> dict:
    return {'app': 'gr-store-app'}

app.include_router(category.router)
app.include_router(products.router)
app.include_router(auth.router)
