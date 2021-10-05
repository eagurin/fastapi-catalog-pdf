import shutil
import uuid
import os

from fastapi import HTTPException


def upload_image(image_file):
    if image_file:
        image_format = image_file.filename.split(".")[-1]
        if not image_format in ["jpeg", "jpg", "png"]:
            raise HTTPException(status_code=415, detail="Unsupported Media Type")
        url = "image/" + str(uuid.uuid4()) + "." + image_format
        with open(url, "wb") as image:
            shutil.copyfileobj(image_file.file, image)
        return url


def delete_file(url: str):
    if os.path.isfile(url):
        os.remove(url)
    else:
        raise HTTPException(status_code=404, detail="File not found")
