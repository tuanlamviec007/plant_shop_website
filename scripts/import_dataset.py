"""
Script để import dữ liệu cây cảnh từ CSV vào database
"""
import os
import sys
import django
import csv

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from products.models import Product, Category
from django.utils.text import slugify


def import_plants():
    """Import plants from CSV file"""
    csv_file = os.path.join(project_dir, 'data', 'plant_dataset.csv')
    
    if not os.path.exists(csv_file):
        print(f"❌ File {csv_file} không tồn tại!")
        return
    
    print("🌱 Bắt đầu import dữ liệu cây cảnh...")
    
    created_count = 0
    updated_count = 0
    error_count = 0
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                # Lấy hoặc tạo category
                category_name = row['category']
                category, _ = Category.objects.get_or_create(
                    name=category_name,
                    defaults={'slug': slugify(category_name)}
                )
                
                # Kiểm tra sản phẩm đã tồn tại chưa
                product_name = row['name']
                product, created = Product.objects.get_or_create(
                    name=product_name,
                    defaults={
                        'slug': slugify(product_name),
                        'category': category,
                        'description': row['description'],
                        'price': 150000,  # Giá mặc định
                        'stock': 100,
                        'care_level': 'easy',
                    }
                )
                
                # Cập nhật thông tin recommendation
                product.light_condition = row['light_condition']
                product.location_type = row['location_type']
                product.space_required = row['space_required']
                product.care_time = row['care_time']
                product.experience_level = row['experience_level']
                product.feng_shui_meaning = row['feng_shui_meaning']
                product.care_tips = row['care_tips']
                
                # Cập nhật description nếu có
                if row['description']:
                    product.description = row['description']
                
                product.save()
                
                if created:
                    created_count += 1
                    print(f"✅ Tạo mới: {product_name}")
                else:
                    updated_count += 1
                    print(f"🔄 Cập nhật: {product_name}")
                    
            except Exception as e:
                error_count += 1
                print(f"❌ Lỗi khi xử lý {row.get('name', 'Unknown')}: {str(e)}")
    
    print("\n" + "="*50)
    print(f"📊 Kết quả import:")
    print(f"   ✅ Tạo mới: {created_count} sản phẩm")
    print(f"   🔄 Cập nhật: {updated_count} sản phẩm")
    print(f"   ❌ Lỗi: {error_count} sản phẩm")
    print("="*50)


if __name__ == '__main__':
    import_plants()
