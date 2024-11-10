from backend.dao.base import BaseDAO

from backend.products.models import Products


class ProductsDAO(BaseDAO):
    model = Products

