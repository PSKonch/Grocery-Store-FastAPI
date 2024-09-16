from sqlalchemy import create_engine
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine('postgresql+asyncpg://grocery:1234@localhost:5432/grocery', echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass
    # relationship нужен для определения переменной, через которую к нам можно обращаться
    # офк должно быть и с обратной стороны
    # uselist=False -> указывает на тип связи 1 к 1. По умолчанию значение uselist=True
    # + relationship указывает на то, какие таблицы мы связываем


