from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.products.router import router as products_router
from backend.images.router import router as images_router

app = FastAPI()

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




