import os
import sys
import json
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plant_shop.settings')
django.setup()

from plant_recommendation.ai_service import chatbot_response
from django.core.serializers.json import DjangoJSONEncoder

if __name__ == "__main__":
    response = chatbot_response("tôi muốn tìm cây trong phòng")
    print(json.dumps(response, cls=DjangoJSONEncoder, ensure_ascii=False, indent=2))
