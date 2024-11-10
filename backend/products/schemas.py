from pydantic import BaseModel


class SProduct(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: str