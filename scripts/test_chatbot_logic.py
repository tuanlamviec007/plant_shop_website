
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from plant_recommendation.ai_service import chatbot_response

def test_chat(message):
    print(f"\n--- User: '{message}' ---")
    response = chatbot_response(message)
    print(f"Bot: {response['message']}")
    if 'data' in response and response['data']:
        print(f"Found {len(response['data'])} products:")
        for p in response['data']:
            print(f" - {p['name']} ({p['price']}) - {p['url']}")
    
    if 'filters_detected' in response:
        print(f"Debug Filters: {response['filters_detected']}")

if __name__ == "__main__":
    # Test cases
    test_chat("Xin chào")
    test_chat("Tìm cây trong nhà dễ chăm sóc")
    test_chat("Cây để bàn làm việc")
    test_chat("Cây ngoài trời nhiều nắng")
    test_chat("Cây abcdxyz không có thật")
