import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from plant_recommendation.ai_service import _extract_intents_and_filters, chatbot_response

texts = ["tôi muốn tìm cây đào", "cây đào"]

for text in texts:
    intent, filters = _extract_intents_and_filters(text)
    print(f"Text: {text} -> Intent: {intent}, Filters: {filters}")
    resp = chatbot_response(text)
    print("Response message:", resp['message'])
    print("-" * 30)
