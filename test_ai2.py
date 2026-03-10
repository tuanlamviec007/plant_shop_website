import os
import sys
import json
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from plant_recommendation.ai_service import chatbot_response

if __name__ == "__main__":
    tests = [
        # 1. General
        "Cây kim tiền là cây gì?",
        "Cây trầu bà có tác dụng gì?",
        "Cây thiết mộc lan có độc không?",
        "Cây vạn niên thanh có phù hợp trồng trong nhà không?",
        
        # 2. Care
        "Cách chăm sóc cây lan ý?",
        "Cây kim ngân cần tưới nước bao nhiêu lần?",
        "Ánh sáng cho cây sung?",
        "Cây thường xuân trồng trong nhà được không?",
        "thay chậu cây phú quý",
        
        # 3. Shopping
        "Giá cây kim tiền bao nhiêu?",
        "Shop có bán cây trầu bà không?",
        
        # 4. Comparison
        "Cây kim tiền và kim ngân khác nhau thế nào?",
        "Nên trồng lan ý hay trầu bà?",
        "So sánh cây vạn niên thanh và cây thiết mộc lan",
        "cây móng rồng" # Unregistered
    ]
    for text in tests:
        print(f"\n--- Testing: {text} ---")
        response = chatbot_response(text)
        print("Mssg:", response.get('message'))
        print("Data size:", len(response.get('data', [])))
