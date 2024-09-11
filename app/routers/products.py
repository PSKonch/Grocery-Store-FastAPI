from typing import List
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from starlette import status

router = APIRouter(prefix='/products', tags=['products'])

class ProductModel(BaseModel):
    id: int = None
    name: str

    


products_db = []

@router.get('/')
async def get_all_products() -> List:
    return products_db

@router.post('/create')
async def create_a_product(product: ProductModel) -> str:
    product.id = len(products_db)
    products_db.append(product)
    return f'{product.id} {product.name} - was created'
    

@router.get('/{category_slug}')
async def product_by_category(category_slug: str):
    ...

@router.get('/product/{product_slug}')
async def product_detail(product_slug: str):
    ...

@router.put('/product/{product_slug}')
async def product_update(product_slug: str):
    ...

@router.delete('/delete')
async def product_delete(product_id: int):
    ...