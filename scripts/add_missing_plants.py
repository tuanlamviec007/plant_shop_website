import os
import sys
import django

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from products.models import Product, Category
from django.utils.text import slugify

# Create Category if needed
category, _ = Category.objects.get_or_create(name='Cây Cảnh Lá', defaults={'slug': 'cay-canh-la'})

# Add Cây Thường Xuân
Product.objects.get_or_create(
    name='Cây Thường Xuân',
    defaults={
        'slug': slugify('Cây Thường Xuân'),
        'category': category,
        'description': 'Cây Thường Xuân thân leo, dễ trồng, mang ý nghĩa may mắn.',
        'price': 80000,
        'stock': 50,
        'care_level': 'easy'
    }
)

# Thêm Cây Sung hoặc đổi tên
Product.objects.get_or_create(
    name='Cây Sung',
    defaults={
        'slug': slugify('Cây Sung'),
        'category': category,
        'description': 'Cây Sung mang ý nghĩa sung túc, viên mãn.',
        'price': 150000,
        'stock': 30,
        'care_level': 'medium'
    }
)

print("Đã thêm Cây Thường Xuân và Cây Sung vào database.")
