from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.admin.views import ProductsAdmin
from backend.database import engine
from backend.products.router import router as products_router
from backend.images.router import router as images_router
from backend.users.router import router_auth, router_users
from sqladmin import Admin
app = FastAPI()

admin = Admin(app, engine)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(images_router)
app.include_router(router_auth)
app.include_router(router_users)
admin.add_view(ProductsAdmin)



