from fastapi import APIRouter

from backend.products.dao import ProductsDAO
from backend.products.schemas import SProduct

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/")
async def get_products():
    return await ProductsDAO.get_all()


@router.get("/{id}")
async def get_product(id: int):
    return await ProductsDAO.get_by_id(id)


@router.post("/create")
async def create_product(product: SProduct):
    return await ProductsDAO.create(**product.dict())


@router.put("/{id}")
async def update_product(id: int, name: str, description: str, price: int, image_url: str):
    return await ProductsDAO.update(id, name=name, description=description, price=price, image_url=image_url)


@router.delete("/delete/{id}")
async def delete_product(id: int):
    return await ProductsDAO.delete(id)