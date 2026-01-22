
import os
from pathlib import Path
from django.conf import settings
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

BASE_DIR = Path(__file__).resolve().parent

image_names = [
    "Cây Kim Tiền.jpg",
    "Cây Lưỡi Hổ.jpg",
    "Cây Trầu Bà Đế Vương.jpg",
    "Sen đá Nâu.jpg",
    "Xương rồng Bát Tiên.jpg",
    "terrarium sa mạc.jpg"
]

print(f"Checking static images in: {settings.BASE_DIR / 'static' / 'images'}")

for name in image_names:
    path = settings.BASE_DIR / 'static' / 'images' / name
    if os.path.exists(path):
        print(f"[OK] Found: {name}")
    else:
        print(f"[MISSING] Could not find: {name} at {path}")
