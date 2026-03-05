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
        "tôi muốn tìm cây đào", 
        "cây abcdxyz",
        "cây móng rồng"
    ]
    for text in tests:
        print(f"\n--- Testing: {text} ---")
        response = chatbot_response(text)
        print("Mssg:", response.get('message'))
        print("Data size:", len(response.get('data', [])))
