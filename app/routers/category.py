from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas import CreateCategory
from app.models.category import Category
from app.models.products import Product

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
async def get_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):

    categories = await db.scalars(select(Category).where(Category.is_active == False))

    return categories.all()



@router.post('/create')
async def create_category(db: Annotated[AsyncSession, Depends(get_db)], create_category: CreateCategory):

    await db.execute(insert(Category).values(name=create_category.name, 
                                       slug=slugify(create_category.name), 
                                       parent_id=create_category.parent_id))
    await db.commit()
    
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Success'
    }



@router.put('/update_category')
async def update_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int, update_category: CreateCategory):

    category = await db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category doesnt exist'
        )

    await db.execute(update(Category).where(Category.id == category_id).values(name=update_category.name, 
                                                                         slug=slugify(update_category.name),
                                                                         parent_id=update_category.parent_id))
    await db.commit()
    
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Success'
    }



@router.delete('/delete')
async def delete_category(db: Annotated[AsyncSession, Depends(get_db)], category_id: int):

    category = await db.scalar(select(Category).where(Category.id == category_id))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category doesnt exist'
        )

    await db.execute(delete(Category).where(Category.id == category_id))
    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Success'
    }