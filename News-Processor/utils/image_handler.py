import os, requests
from urllib.parse import urlparse
from PIL import Image, ImageDraw

def handle_aricle_image(url, folder_path, article_id):
    if not url:
        return create_error_png(folder_path, article_id)
    

    try:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        extension = os.path.splitext(filename)[-1] or "jpg"
        image_filename = f"{article_id}_{filename}"
        image_path = os.path.join(folder_path, image_filename)

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
    except Exception:
        return create_error_png(folder_path, article_id)
    

def create_error_png(folder_path, article_id):
    image_path = os.path.join(folder_path, f"{article_id}_error.png")
    img = Image.new("RGB", (600, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((200, 180), "error", fill=(255, 0, 0))
    img.save(image_path)
    return image_path 