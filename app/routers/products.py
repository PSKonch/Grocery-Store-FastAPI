from typing import List, Annotated
from fastapi import APIRouter, Body, HTTPException, Depends, status
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from slugify import slugify

from app.models.category import Category
from app.models.products import Product
from app.schemas import CreateProduct
from app.backend.db_depends import get_db

router = APIRouter(prefix='/products', tags=['products'])

@router.get('/')
async def get_all_products(db: Annotated[Session, Depends(get_db)]):

    products = db.scalars(select(Product).where(Product.is_active == False))

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes'
    }



@router.post('/create')
async def create_a_product(db: Annotated[Session, Depends(get_db)], create_product: CreateProduct):

    db.execute(insert(Product).values(name = create_product.name, 
                                      description = create_product.description, 
                                      slug = slugify(create_product.name), 
                                      rating = create_product.rating))
    db.commit()

    return {
        'status': status.HTTP_201_CREATED,
        'transaction': 'Succes'
    }



@router.get('/{category_slug}')
async def product_by_category(db: Annotated[Session, Depends(get_db)], category_slug: str):

    category = db.scalar(select(Category).where(Category.slug == category_slug))
    products = db.scalars(select(Product).where(Product.category_id == category.id)).all()

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes'
    }



@router.get('/product/{product_slug}')
async def product_detail(db: Annotated[Session, Depends(get_db)], product_slug: str):

    product = db.scalar(select(Product).where(Product.slug == product_slug))

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes'
    }



@router.put('/product/{product_slug}')
async def product_update(product_slug: str, db: Annotated[Session, Depends(get_db)], update_product: CreateProduct):

    db.execute(update(Product).where(Product.slug == product_slug).values(name=update_product.name,
                                                                          description=update_product.description, 
                                                                          rating=update_product.rating,
                                                                          slug=slugify(update_product.name)))
    db.commit()
    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes'
    }



@router.delete('/delete')
async def product_delete(product_id: int, db: Annotated[Session, Depends(get_db)]):
    
    db.execute(delete(Product).where(Product.id == product_id))
    db.commit()

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes'
    }