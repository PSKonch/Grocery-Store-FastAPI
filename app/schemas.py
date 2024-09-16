from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    rating: float
    category_id: int

class CreateCategory(BaseModel):
    name: str
    parent_id: int | None