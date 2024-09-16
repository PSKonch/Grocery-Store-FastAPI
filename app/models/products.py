from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Product(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    rating = Column(Float)
    is_active = Column(Boolean, default=True)   

    supplier_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    category_id = Column(Integer, ForeignKey('categories.id')) 
    # на стороне получателя связи нужен импорт этой таблицы (модели)
    # пример:
    # category_id связан с Category, внутри файла, где описана таблица Category 
    # должен быть импорт from app.routers.products import Product
    # На обратной стороне это не нужно, несмотря на relationship с указанием нужной нам таблицы
    
    category = relationship('Category', back_populates='products')

