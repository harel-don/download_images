import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Use a session with a browser-like User-Agent
SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/104.0.0.0 Safari/537.36'
    )
})


def is_valid_extension(url, exts):
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    return ext in exts


def get_image_urls(page_url):
    try:
        r = SESSION.get(page_url, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️  Failed to load page: {e}")
        return []
    soup = BeautifulSoup(r.text, 'html.parser')

    urls = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if not src:
            continue
        urls.append(urljoin(page_url, src))
    return urls


def download_image(url, size):
    try:
        r = SESSION.get(url, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️  Error downloading {url}: {e}")
        return False, None

    data = r.content
    try:
        img = Image.open(BytesIO(data))
    except IOError:
        print(f"⚠️  Invalid image data: {url}")
        return False, None

    return (list(img.size) == size), (img, data)


def save_image(img_tuple, src_url, out_dir):
    img, raw = img_tuple
    fn = os.path.basename(urlparse(src_url).path)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, fn)
    ext = fn.lower().split('.')[-1]

    if ext in ('gif','png'):
        with open(path, 'wb') as f:
            f.write(raw)
    else:
        img.save(path)
    print(f"✅ Saved {fn}")