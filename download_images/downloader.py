import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
from io import BytesIO

CONFIG = {
    "extensions": [".gif", ".png"],
    "size": (96, 96),
}


def is_valid_extension(url, extensions):
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    return ext in extensions


def get_image_urls(page_url):
    resp = requests.get(page_url); resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return [
        urljoin(page_url, img["src"])
        for img in soup.find_all("img")
        if img.get("src")
    ]


def download_image(url, size):
    resp = requests.get(url); resp.raise_for_status()
    data = resp.content
    img = Image.open(BytesIO(data))
    return (img.size == size), (img, data)


def save_image(img_tuple, src_url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    img, raw = img_tuple
    filename = os.path.basename(urlparse(src_url).path)
    path = os.path.join(output_dir, filename)
    ext = filename.lower().split('.')[-1]

    if ext in ("gif", "png"):
        with open(path, "wb") as f:
            f.write(raw)
    else:
        img.save(path)
    print(f"Saved {filename}")