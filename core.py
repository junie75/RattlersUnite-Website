from PIL import Image
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
from globals import UPLOAD_FOLDER


def compress_image(img_path, quality=60):
    img = Image.open(img_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(img_path, optimize=True, quality=quality)


def save_image(image, folder):
    if image:
        filename = secure_filename(str(uuid4()) + "_" + image.data.filename)
        db_path = f"{folder}/{filename}"
        full_path = os.path.join(UPLOAD_FOLDER, db_path)
        image.data.save(full_path)
        compress_image(full_path)

        return db_path
    return None


def clean_image_folder(old_image, banner=True):
    if banner:
        if old_image != f"../static/defaults/STMUlogo.png":
            os.remove(f"uploads/{old_image}")
    else:
        if old_image != f"../static/defaults/STMUlogo.jpg":
            os.remove(f"uploads/{old_image}")
