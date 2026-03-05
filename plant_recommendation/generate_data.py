import os
import sys
import json
import django
import random

# Thiết lập môi trường Django
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from products.models import Product

def generate_training_data():
    # Lấy ngẫu nhiên 10 sản phẩm đang active
    products = list(Product.objects.filter(is_active=True).order_by('?')[:10])
    
    if len(products) < 1:
        print("Không có sản phẩm nào trong database!")
        return

    print("Đã chọn ngẫu nhiên 10 cây:")
    for p in products:
        print(f"- {p.name} (Location: {p.location_type}, Care: {p.care_level})")
    
    training_data = []

    # 1. Intent: greeting
    greetings = [
        "chào shop", "hi", "hello", "xin chào", "chào bạn",
        "có ai ở đây không", "shop ơi", "alo", "chào buổi sáng"
    ]
    for text in greetings:
        training_data.append({"text": text, "intent": "greeting"})

    # 2. Intent: recommendation
    recommends = [
        "tư vấn cho mình với", "mình muốn mua cây", "shop gợi ý cây đi",
        "có cây nào đẹp không", "giới thiệu vài cây xem nào",
        "tìm giúp mình một cây", "mình cần mua cây cảnh", "bán cho mình cây"
    ]
    for text in recommends:
        training_data.append({"text": text, "intent": "recommendation"})
        
    # 3. Intent: ask_specific_plant (Dựa vào 10 cây ngẫu nhiên)
    for p in products:
        name_lower = p.name.lower()
        phrases = [
            f"mình muốn mua {name_lower}",
            f"có bán {name_lower} không",
            f"giá {name_lower} bao nhiêu",
            f"cho xem {name_lower} với",
            f"tìm {name_lower}",
            f"hỏi về {name_lower}",
            f"{name_lower} còn hàng không shop",
            name_lower
        ]
        for text in phrases:
            # We add entity annotations or just simple intent
            training_data.append({
                "text": text, 
                "intent": "ask_specific_plant",
                "entities": {"plant_name": name_lower} # Optional for logic processing
            })

    # 4. Intent: find_by_location
    location_phrases = {
        "indoor": ["cây để trong nhà", "cây trồng trong phòng", "cây nội thất", "cây để bàn làm việc", "cây văn phòng"],
        "outdoor": ["cây trồng ngoài trời", "cây sân vườn", "cây ban công", "cây trồng trước hiên"],
        "both": ["cây nào cũng được", "trồng đâu cũng sống"]
    }
    for loc, phrases in location_phrases.items():
        for text in phrases:
            training_data.append({"text": text, "intent": "find_by_location", "entities": {"location_type": loc}})
            
    # Mix and match with Recommendation
    for loc, phrases in location_phrases.items():
        for text in phrases:
            training_data.append({"text": f"tư vấn {text}", "intent": "find_by_location", "entities": {"location_type": loc}})
            training_data.append({"text": f"cho mình xem {text}", "intent": "find_by_location", "entities": {"location_type": loc}})

    # 5. Intent: find_by_care_level
    care_phrases = {
        "easy": ["cây dễ chăm", "cây ít chăm sóc", "cây cho người lười", "cây sống dai", "cây dễ sống", "cây không cần chăm nhiều"],
        "medium": ["cây chăm sóc trung bình", "cây bình thường"],
        "hard": ["cây khó chăm", "cây cần chăm sóc kỹ", "cây đẹp mà khó chăm"]
    }
    for care, phrases in care_phrases.items():
        for text in phrases:
            training_data.append({"text": text, "intent": "find_by_care_level", "entities": {"care_level": care}})

    # Mix and match location and care level? Keep it simple for TF-IDF.
    
    # Save to JSON
    output_path = os.path.join(script_dir, "training_data.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=4)
        
    print(f"Đã tạo {len(training_data)} mẫu dữ liệu huấn luyện tại {output_path}")
    
    # Save the 10 selected plants for reference in training / logic
    selected_plants = [{"id": p.id, "name": p.name.lower(), "slug": p.slug} for p in products]
    config_path = os.path.join(script_dir, "selected_plants.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(selected_plants, f, ensure_ascii=False, indent=4)
        
    print(f"Đã lưu danh sách 10 cây ngẫu nhiên tại {config_path}")

if __name__ == "__main__":
    generate_training_data()
