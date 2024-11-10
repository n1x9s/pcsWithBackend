import shutil
import requests

from fastapi import APIRouter

router = APIRouter(
    prefix="/images",
    tags=["images"],
)

@router.post("/upload/")
async def upload_image(name: str, url: str):
    im_path = f'backend/static/images/{name}.jpg'
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(im_path, "wb+") as file_obj:
            shutil.copyfileobj(response.raw, file_obj)
    else:
        return {"error": "Failed to download image"}
    return {"message": "Image uploaded successfully"}