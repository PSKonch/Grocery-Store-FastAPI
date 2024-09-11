from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    slug: str

class CreateCategory(BaseModel):
    name: str
    parent_id: int | None