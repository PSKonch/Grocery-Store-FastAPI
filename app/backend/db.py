from sqlalchemy import create_engine
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine('sqlite///grocery.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = 'user' 

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(50))

    profile = relationship('Profile', uselist=False, back_populates='user') 
    # relationship нужен для определения переменной, через которую к нам можно обращаться
    # офк должно быть и с обратной стороны
    # uselist=False -> указывает на тип связи 1 к 1. По умолчанию значение uselist=True
    # + relationship указывает на то, какие таблицы мы связываем


class Profile(Base):

    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id')) # установка связи с таблицей User от таблицы Profile

    user = relationship('User', back_populates='profile') 