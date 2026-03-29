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
    plants_req = [
        'Cây Kim Tiền', 'Cây Lưỡi Hổ', 'Cây Kim Ngân', 'Cây Thường Xuân', 
        'Cây Thiết Mộc Lan', 'Cây Vạn Niên Thanh', 'Cây Trầu Bà', 
        'Cây Phú Quý', 'Cây Lan Ý', 'Cây Sung'
    ]
    
    # Lấy chính xác 10 cây
    products = []
    for name in plants_req:
        p = Product.objects.filter(name__icontains=name).first()
        if p:
            products.append(p)
            
    if len(products) < 10:
        print(f"Cảnh báo: Chỉ tìm thấy {len(products)}/10 cây cần thiết trong database!")

    print("Danh sách cây sẽ sử dụng:")
    for p in products:
        print(f"- {p.name}")
    
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
        
    # Sinh dữ liệu cho từng cây
    for p in products:
        name_lower = p.name.lower()
        
        # --- Danh mục 3: Câu hỏi Mua Hàng (Shopping) ---
        # Intent: ask_specific_plant
        phrases_shopping = [
            f"giá {name_lower} bao nhiêu",
            f"shop có bán {name_lower} không",
            f"{name_lower} còn hàng không",
            f"tôi muốn mua {name_lower}",
            f"{name_lower} có size nào",
            f"{name_lower} giá bao nhiêu tiền",
            f"cho xem {name_lower} với",
            f"tìm {name_lower}",
            name_lower
        ]
        for text in phrases_shopping:
            training_data.append({
                "text": text, 
                "intent": "ask_specific_plant",
                "entities": {"plant_name": name_lower}
            })
            
        # --- Danh mục 1: Câu hỏi Chung (General) ---
        # Intent: ask_plant_characteristics (characteristic_type = general)
        phrases_general = [
            f"{name_lower} là cây gì",
            f"đặc điểm của {name_lower} là gì",
            f"đặc điểm {name_lower}",
            f"{name_lower} có ý nghĩa phong thủy gì",
            f"ý nghĩa phong thủy {name_lower}",
            f"{name_lower} có dễ trồng không",
            f"{name_lower} có phù hợp trồng trong nhà không",
            f"trồng {name_lower} trong nhà",
            f"{name_lower} có độc không",
            f"{name_lower} có tác dụng gì",
            f"hỏi về {name_lower}",
            f"thông tin {name_lower}"
        ]
        for text in phrases_general:
             training_data.append({
                "text": text, 
                "intent": "ask_plant_characteristics",
                "entities": {"plant_name": name_lower}
            })
             
        # --- Danh mục 2: Câu hỏi Chăm Sóc (Care) ---
        # Intent: ask_plant_characteristics (characteristic_type = care/water/light...)
        phrases_care = [
            f"cách chăm sóc {name_lower}",
            f"chăm sóc {name_lower} như thế nào",
            f"cách chăm {name_lower}",
            f"{name_lower} cần tưới nước bao nhiêu lần",
            f"{name_lower} tưới nước sao",
            f"tưới {name_lower} như nào",
            f"{name_lower} cần ánh sáng như thế nào",
            f"ánh sáng cho {name_lower}",
            f"{name_lower} cần nắng không",
            f"{name_lower} có cần bón phân không",
            f"bón phân cho {name_lower}",
            f"nhiệt độ thích hợp cho {name_lower}",
            f"{name_lower} chịu nhiệt độ",
            f"{name_lower} trồng trong nhà được không",
            f"{name_lower} có cần thay chậu không",
            f"thay chậu {name_lower}"
        ]
        for text in phrases_care:
             training_data.append({
                "text": text, 
                "intent": "ask_plant_characteristics",
                "entities": {"plant_name": name_lower}
            })

    # --- Danh mục 4: Câu hỏi So Sánh (Comparison) ---
    # Intent: compare_plants
    for i in range(len(products)):
        for j in range(i + 1, len(products)):
            p1 = products[i].name.lower()
            p2 = products[j].name.lower()
            
            phrases_comparison = [
                f"{p1} và {p2} khác nhau như thế nào",
                f"nên trồng {p1} hay {p2}",
                f"cây nào dễ chăm hơn: {p1} hay {p2}",
                f"so sánh {p1} và {p2}",
                f"{p1} với {p2} nên mua cây nào"
            ]
            
            for text in phrases_comparison:
                training_data.append({
                    "text": text, 
                    "intent": "compare_plants",
                    "entities": {"plant_1": p1, "plant_2": p2}
                })

    # Intent: find_by_location
    location_phrases = {
        "indoor": [
            "cây để trong nhà", "cây trồng trong phòng", "cây nội thất",
            "cây để bàn làm việc", "cây văn phòng", "cây để bàn",
            "cây trong nhà", "cây phòng khách", "cây phòng ngủ",
            "cây trồng trong nhà", "cây chịu bóng"
        ],
        "outdoor": [
            "cây trồng ngoài trời", "cây sân vườn", "cây ban công",
            "cây trồng trước hiên", "cây ngoài trời", "cây trước cổng",
            "cây trồng ngoài", "cây cho vườn"
        ],
        "both": ["cây nào cũng được", "trồng đâu cũng sống", "cây trồng được trong và ngoài"]
    }
    location_prefixes = [
        "", "tư vấn ", "cho mình xem ", "tìm giúp mình ",
        "gợi ý ", "tìm cho tôi ", "tìm cho tôi 5 ",
        "tìm cho tôi 4 ", "gợi ý cho tôi ", "cần mua ",
        "mình muốn ", "mình cần ", "tìm "
    ]
    for loc, phrases in location_phrases.items():
        for text in phrases:
            for prefix in location_prefixes:
                training_data.append({
                    "text": f"{prefix}{text}".strip(),
                    "intent": "find_by_location",
                    "entities": {"location_type": loc}
                })

    # Intent: find_by_care_level
    care_phrases = {
        "easy": [
            "cây dễ chăm", "cây ít chăm sóc", "cây cho người lười",
            "cây sống dai", "cây dễ sống", "cây không cần chăm nhiều",
            "cây dễ nuôi", "cây cho người bận rộn", "cây ít tưới nước",
            "cây dễ trồng", "cây dễ chăm sóc nhất"
        ],
        "medium": [
            "cây chăm sóc trung bình", "cây bình thường",
            "cây không quá khó không quá dễ"
        ],
        "hard": [
            "cây khó chăm", "cây cần chăm sóc kỹ",
            "cây đẹp mà khó chăm", "cây cần nhiều công chăm sóc"
        ]
    }
    care_prefixes = [
        "", "tìm ", "gợi ý ", "tìm cho tôi ", "cho mình xem ",
        "tôi cần ", "mình muốn "
    ]
    for care, phrases in care_phrases.items():
        for text in phrases:
            for prefix in care_prefixes:
                training_data.append({
                    "text": f"{prefix}{text}".strip(),
                    "intent": "find_by_care_level",
                    "entities": {"care_level": care}
                })

    # Save to JSON
    output_path = os.path.join(script_dir, "training_data.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=4)
        
    print(f"Đã tạo {len(training_data)} mẫu dữ liệu huấn luyện tại {output_path}")
    
    # Save the selected plants for reference in training / logic
    selected_plants = [{"id": p.id, "name": p.name.lower(), "slug": p.slug} for p in products]
    config_path = os.path.join(script_dir, "selected_plants.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(selected_plants, f, ensure_ascii=False, indent=4)
        
    print(f"Đã lưu danh sách {len(products)} cây tại {config_path}")

if __name__ == "__main__":
    generate_training_data()
