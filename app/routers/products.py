from typing import List
from fastapi import APIRouter, Body, HTTPException
from starlette import status

router = APIRouter(prefix='/products', tags=['products'])

@router.get('/')
async def get_all_products():
    ...

@router.post('/create')
async def create_a_product():
    ...
    

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