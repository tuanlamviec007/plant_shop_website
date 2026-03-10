import os, sys, django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()
from products.models import Product, Category
from django.utils.text import slugify

plants_req = [
    'Cây kim tiền', 'Cây lưỡi hổ', 'Cây kim ngân', 'Cây thường xuân', 
    'Cây thiết mộc lan', 'Cây vạn niên thanh', 'Cây trầu bà', 
    'Cây phú quý', 'Cây lan ý', 'Cây sung'
]

# Pick any category or create
cat = Category.objects.first()
if not cat:
    cat = Category.objects.create(name='Cây tự động tạo', slug='cay-tu-dong-tao')

print("--- CHECKING PLANTS ---")
for name in plants_req:
    p = Product.objects.filter(name__icontains=name).first()
    if p:
        print(f"FOUND: {p.name} (id={p.id})")
        # Ensure it's active
        if not p.is_active:
            p.is_active = True
            p.save()
            print(f"  -> Activated {p.name}")
    else:
        print(f"MISSING: {name}")
        # Create a basic one
        slug = slugify(name)
        # Handle potentional slug collision
        if Product.objects.filter(slug=slug).exists():
            slug += '-1'
            
        p = Product.objects.create(
            category=cat,
            name=name,
            slug=slug,
            description=f"Đây là {name}.",
            price=150000,
            stock=100,
            image='', 
            is_active=True
        )
        print(f"  -> Created {name} (id={p.id})")

print("--- DONE ---")
