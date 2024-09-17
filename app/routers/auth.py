from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from typing import Annotated
from passlib.context import CryptContext

from app.models.user import User
from app.schemas import CreateUser
from app.backend.db_depends import get_db

router = APIRouter(prefix='/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def auth_user(db: Annotated[AsyncSession, Depends(get_db)], username: str, password: str):

    user = await db.scalar(select(User).where(User.username == username))
    
    if (not user) or (not user.is_active) or (not bcrypt_context.verify(password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    return user


@router.post('/token')
async def login(db: Annotated[AsyncSession, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = await auth_user(db, form_data.username, form_data.password)
    
    return {
        'access_token': user.username,
        'token_type': 'bearer'
    }



@router.get('/me')
async def read_current_user(user: User = Depends(oauth2_scheme)):

    return user


@router.post('/')
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], create_user: CreateUser):

    await db.execute(insert(User).values(first_name = create_user.first_name, 
                                         last_name = create_user.last_name, 
                                         username = create_user.username, 
                                         email = create_user.email, 
                                         hashed_password = bcrypt_context.hash(create_user.password)))
    await db.commit()

    return {
        'status': status.HTTP_201_CREATED,
        'transaction': 'success'
    }