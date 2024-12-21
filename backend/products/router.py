from typing import Optional

from fastapi import APIRouter, Query, HTTPException, status, Depends

from backend.products.dao import ProductsDAO
from backend.products.schemas import SProduct
from backend.users.dependencies import get_current_user
from backend.users.models import Users

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/")
async def get_products(
        search: Optional[str] = Query(None, description="Поиск по названию продукта"),
        sort_by: Optional[str] = Query(None, description="Сортировка по цене: 'asc' или 'desc'")
):
    return await ProductsDAO.get_all(search=search, sort_by=sort_by)


@router.get("/{id}")
async def get_product(id: int):
    return await ProductsDAO.get_by_id(id)


@router.post("/create")
async def create_product(product: SProduct, current_user: Users = Depends(get_current_user)):
    if current_user.email != "prodavec@gmail.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to add products"
        )
    return await ProductsDAO.create(**product.dict())


@router.put("/update/{id}")
async def update_product(id: int, name: str, description: str, price: int, image_url: str):
    return await ProductsDAO.update(id, name=name, description=description, price=price, image_url=image_url)


@router.delete("/delete/{id}")
async def delete_product(id: int):
    return await ProductsDAO.delete(id)


@router.post("/purchase/{id}")
async def purchase_product(id: int):
    result = await ProductsDAO.purchase_product(id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result
