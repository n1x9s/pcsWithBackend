from sqladmin import ModelView

from backend.products.models import Products


class ProductsAdmin(ModelView, model=Products):
    column_list = ('id', 'name', 'description', 'price', 'image_url')