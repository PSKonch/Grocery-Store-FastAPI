from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from typing import Annotated
from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas import CreateCategory
from app.models.category import Category
from app.models.products import Product

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/all_categories')
async def get_all_categories(db: Annotated[Session, Depends(get_db)]):

    categories = db.scalars(select(Category).where(Category.is_active == False)).all()

    return categories  



@router.post('/create')
async def create_category(db: Annotated[Session, Depends(get_db)], create_category: CreateCategory):

    db.execute(insert(Category).values(name=create_category.name, 
                                       slug=slugify(create_category.name), 
                                       parent_id=create_category.parent_id))
    db.commit()
    
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Success'
    }



@router.put('/update_category')
async def update_category(db: Annotated[Session, Depends(get_db)], category_id: int, update_category: CreateCategory):

    db.execute(update(Category).where(Category.id == category_id).values(name=update_category.name, 
                                                                         slug=slugify(update_category.name),
                                                                         parent_id=update_category.parent_id))
    db.commit()
    
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Success'
    }



@router.delete('/delete')
async def delete_category(db: Annotated[Session, Depends(get_db)], category_id: int):

    db.execute(delete(Category).where(Category.id == category_id))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Success'
    }