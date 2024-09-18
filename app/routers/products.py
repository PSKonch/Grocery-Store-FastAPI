from typing import List, Annotated
from fastapi import APIRouter, Body, HTTPException, Depends, status
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify

from app.models.category import Category
from app.models.products import Product
from app.schemas import CreateProduct
from app.backend.db_depends import get_db

router = APIRouter(prefix='/products', tags=['products'])

@router.get('/')
async def get_all_products(db: Annotated[AsyncSession, Depends(get_db)]):

    products = await db.scalars(select(Product).where(Product.is_active == True))

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes',
        'products': list(products)
    }



@router.post('/create')
async def create_a_product(db: Annotated[AsyncSession, Depends(get_db)], create_product: CreateProduct):

    await db.execute(insert(Product).values(name = create_product.name, 
                                      description = create_product.description, 
                                      slug = slugify(create_product.name), 
                                      rating = create_product.rating,
                                      category_id = create_product.category_id))
    await db.commit()

    return {
        'status': status.HTTP_201_CREATED,
        'transaction': 'Succes'
    }



@router.get('/{category_slug}')
async def product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):

    category = await db.scalar(select(Category).where(Category.slug == category_slug))

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )
    
    subcategories = await db.scalars(select(Category).where(Category.parent_id == category.id))
    sub_cat = [category.id] + [i.id for i in subcategories]

    products_categories = await db.scalars(select(Product).where(Product.category_id.in_(sub_cat), Product.is_active == True))

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes',
        'db': products_categories
    }



@router.get('/product/{product_slug}')
async def product_detail(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):

    product = await db.scalar(select(Product).where(Product.slug == product_slug))

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product doesnt exist'
        )

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes',
        'product_detail': product
    }



@router.put('/product/{product_slug}')
async def product_update(product_slug: str, db: Annotated[AsyncSession, Depends(get_db)], update_product: CreateProduct):

    product = await db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product doesnt exist'
        )

    await db.execute(update(Product).where(Product.slug == product_slug).values(name=update_product.name,
                                                                          description=update_product.description, 
                                                                          rating=update_product.rating,
                                                                          slug=slugify(update_product.name)))
    await db.commit()

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes'
    }



@router.delete('/delete')
async def product_delete(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]):

    product = await db.scalar(select(Product).where(Product.id == product_id))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product doesnt exist'
        )

    await db.execute(delete(Product).where(Product.id == product_id))
    await db.commit()

    return {
        'status': status.HTTP_200_OK,
        'transaction': 'Succes'
    }