"""
Script to list all products and identify non-Vietnamese plants
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from products.models import Product, Category

print("="*60)
print("DANH SÁCH TẤT CẢ CÂY CẢNH TRONG DATABASE")
print("="*60)

products = Product.objects.all().select_related('category')
print(f"\nTổng số: {products.count()} cây\n")

vietnamese_plants = [
    'Mai Vàng', 'Quất', 'Đào', 'Kim Ngân', 'Phát Tài', 'Lưỡi Hổ',
    'Trầu Bà', 'Lan Ý', 'Hoa Hồng', 'Hoa Giấy', 'Lộc Vừng',
    'Thiết Mộc Lan', 'Cau Tiểu Trâm', 'Tùng La Hán', 'Ngọc Ngân',
    'Hạnh Phúc', 'Vạn Niên Thanh', 'Hoa Lan', 'Trúc Nhật', 'Dương Xỉ',
    'Bàng Singapore', 'Hoa Sứ', 'Tùng Thơm', 'Lá Bỏng', 'Hồng Môn',
    'Trầu Không', 'Phú Quý', 'Ngũ Gia Bì', 'Móng Rồng', 'Tùng Bồng Lai'
]

to_delete = []
to_keep = []

for product in products:
    name = product.name.replace('Cây ', '')
    is_vietnamese = any(vn_name in name for vn_name in vietnamese_plants)
    
    if is_vietnamese:
        to_keep.append(product)
        print(f"✅ KEEP: ID {product.id:3d} - {product.name:30s} ({product.category.name})")
    else:
        to_delete.append(product)
        print(f"❌ DELETE: ID {product.id:3d} - {product.name:30s} ({product.category.name})")

print("\n" + "="*60)
print(f"📊 THỐNG KÊ:")
print(f"   ✅ Giữ lại: {len(to_keep)} cây (Việt Nam)")
print(f"   ❌ Xóa: {len(to_delete)} cây (không phải Việt Nam)")
print("="*60)

if to_delete:
    print("\n🗑️  CÁC CÂY SẼ BỊ XÓA:")
    for p in to_delete:
        print(f"   - {p.name}")
    
    confirm = input("\n⚠️  Bạn có chắc chắn muốn xóa các cây này? (yes/no): ")
    if confirm.lower() == 'yes':
        from orders.models import OrderItem, Cart
        
        count = len(to_delete)
        for p in to_delete:
            # Set OrderItem product to NULL instead of deleting
            OrderItem.objects.filter(product=p).update(product=None)
            # Delete Cart items
            Cart.objects.filter(product=p).delete()
            # Now safe to delete product
            p.delete()
        
        print(f"\n✅ Đã xóa {count} cây cảnh không phải Việt Nam!")
        print("   (OrderItem references đã được set to NULL)")
    else:
        print("\n❌ Hủy thao tác xóa.")
else:
    print("\n✅ Không có cây nào cần xóa!")
