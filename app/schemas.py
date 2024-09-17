from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    rating: float
    category_id: int

class CreateCategory(BaseModel):
    name: str
    parent_id: int | None

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str