"""
Script to update location_type, space_required, feng_shui_meaning for all 10 selected plants.
Phân loại:
- 'desk': location_type=indoor, space_required=small (cây để bàn)
- 'room': location_type=indoor, space_required=medium/large (cây đặt trong phòng, không để bàn)
- 'outdoor/both': cây ngoài trời
"""
import os
import sys
import django

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from products.models import Product

plants_data = [
    {
        "name_contains": "Kim Tiền",
        "location_type": "indoor",
        "space_required": "small",       # ĐỂ BÀN: nhỏ gọn, để bàn được
        "care_time": "low",
        "light_condition": "medium",
        "feng_shui_meaning": "wealth|luck",
        "care_tips": "Tưới nước 1-2 lần/tuần. Đặt nơi có ánh sáng gián tiếp. Bón phân loãng 2 tháng/lần."
    },
    {
        "name_contains": "Lưỡi Hổ",
        "location_type": "indoor",
        "space_required": "medium",      # PHÒNG: cao lớn, KHÔNG ĐỂ BÀN
        "care_time": "low",
        "light_condition": "low",
        "feng_shui_meaning": "air_purifying|health",
        "care_tips": "Tưới nước 1 lần/tuần. Chịu bóng rất tốt. Tránh tưới quá nhiều."
    },
    {
        "name_contains": "Kim Ngân",
        "location_type": "indoor",
        "space_required": "small",       # ĐỂ BÀN
        "care_time": "low",
        "light_condition": "medium",
        "feng_shui_meaning": "wealth|air_purifying",
        "care_tips": "Chịu bóng tốt. Tưới 1-2 lần/tuần. Dễ chăm sóc cho người mới."
    },
    {
        "name_contains": "Thường Xuân",
        "location_type": "indoor",
        "space_required": "small",       # ĐỂ BÀN / LEO TƯỜNG
        "care_time": "low",
        "light_condition": "medium",
        "feng_shui_meaning": "luck",
        "care_tips": "Tưới nước 2-3 lần/tuần. Đặt nơi thoáng mát. Có thể treo hoặc để bàn."
    },
    {
        "name_contains": "Thiết Mộc Lan",
        "location_type": "indoor",
        "space_required": "small",       # ĐỂ BÀN
        "care_time": "low",
        "light_condition": "low",
        "feng_shui_meaning": "air_purifying|health",
        "care_tips": "Chịu bóng. Tưới nước 1-2 lần/tuần. Bón phân loãng 1 tháng/lần."
    },
    {
        "name_contains": "Vạn Niên Thanh",
        "location_type": "indoor",
        "space_required": "small",       # ĐỂ BÀN
        "care_time": "low",
        "light_condition": "low",
        "feng_shui_meaning": "health|air_purifying",
        "care_tips": "Chịu bóng tốt. Tưới ít. Rất phù hợp cho người bận rộn."
    },
    {
        "name_contains": "Trầu Bà",
        "location_type": "indoor",
        "space_required": "small",       # ĐỂ BÀN / TREO
        "care_time": "low",
        "light_condition": "low",
        "feng_shui_meaning": "air_purifying",
        "care_tips": "Ưa bóng râm. Tưới khi đất khô. Phun sương lên lá thường xuyên."
    },
    {
        "name_contains": "Phú Quý",
        "location_type": "indoor",
        "space_required": "medium",      # PHÒNG KHÁCH: cần chậu lớn hơn
        "care_time": "low",
        "light_condition": "medium",
        "feng_shui_meaning": "wealth|luck",
        "care_tips": "Ánh sáng gián tiếp. Tưới đều đặn. Thay nước nếu trồng thủy canh."
    },
    {
        "name_contains": "Lan Ý",
        "location_type": "indoor",
        "space_required": "medium",      # PHÒNG: lá to, cần không gian
        "care_time": "low",
        "light_condition": "low",
        "feng_shui_meaning": "luck|air_purifying",
        "care_tips": "Chịu bóng tốt. Tưới 2-3 lần/tuần. Lau lá để tránh bụi bám."
    },
    {
        "name_contains": "Sung",
        "location_type": "both",
        "space_required": "medium",      # CẢ HAI
        "care_time": "medium",
        "light_condition": "medium",
        "feng_shui_meaning": "prosperity|luck",
        "care_tips": "Ánh sáng tốt. Tưới vừa phải. Phù hợp cả trong nhà và ngoài trời."
    },
]

updated = []
for data in plants_data:
    p = Product.objects.filter(name__icontains=data['name_contains']).first()
    if p:
        p.location_type = data['location_type']
        p.space_required = data['space_required']
        p.care_time = data['care_time']
        p.light_condition = data['light_condition']
        p.feng_shui_meaning = data['feng_shui_meaning']
        p.care_tips = data['care_tips']
        p.save()
        placement = "de ban" if data['space_required'] == 'small' else "phong/ngoai troi"
        updated.append(f"Updated: {p.name} ({data['location_type']}, {data['space_required']} -> {placement})")
    else:
        updated.append(f"NOT FOUND: {data['name_contains']}")

for line in updated:
    print(line)

print(f"\nDone! Updated {len([u for u in updated if u.startswith('Updated')])} plants.")
