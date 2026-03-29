import os
import sys
import django

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from products.models import Product

plants_req = [
    'Cây kim tiền', 'Cây lưỡi hổ', 'Cây kim ngân', 'Cây thường xuân', 
    'Cây thiết mộc lan', 'Cây vạn niên thanh', 'Cây trầu bà', 
    'Cây phú quý', 'Cây lan ý', 'Cây sung'
]

print("Plants in DB:")
for p in Product.objects.all():
    print(f" - {p.name}")

print("\nMissing ones:")
for req in plants_req:
    p = Product.objects.filter(name__icontains=req).first()
    if p:
        print(f"FOUND: {req} -> {p.name}")
    else:
        print(f"MISSING: {req}")
