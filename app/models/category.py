from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.backend.db import Base
from app.models.products import Product


class Category(Base):
    
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=False)

    category = relationship('Product', back_populates='category')

from sqlalchemy.schema import CreateTable
print(CreateTable(Product.__table__))
print(CreateTable(Category.__table__))