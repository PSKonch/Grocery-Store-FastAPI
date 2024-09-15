from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    rating: float

class CreateCategory(BaseModel):
    name: str
    parent_id: int | None