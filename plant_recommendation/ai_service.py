"""
AI Recommendation Service - NLP Implementation
"""
import os
import json
import unicodedata
import re
import joblib
import underthesea
from django.conf import settings
from django.db.models import Q
from products.models import Product

# Path to config file
CONFIG_PATH = os.path.join(settings.BASE_DIR, 'plant_recommendation', 'chatbot_config.json')
MODEL_PATH = os.path.join(settings.BASE_DIR, 'plant_recommendation', 'intent_model.pkl')
PLANTS_PATH = os.path.join(settings.BASE_DIR, 'plant_recommendation', 'selected_plants.json')

_config = None
_model = None
_plants = None

def _load_resources():
    global _config, _model, _plants
    if _config is None:
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                _config = json.load(f)
        except Exception:
            _config = {"intents": {}, "filters": {}}
    if _model is None:
        try:
            _model = joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"❌ Model load error: {e}")
    if _plants is None:
        try:
            with open(PLANTS_PATH, 'r', encoding='utf-8') as f:
                _plants = json.load(f)
        except Exception:
            _plants = []
    return _config, _model, _plants

def _normalize_text(text):
    """Normalize text: lowercase, remove some special chars but KEEP accents"""
    if not text:
        return ""
    text = text.lower()
    # Remove punctuation but keep accented characters. 
    # Just simple regex for word chars and spaces
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def _extract_intents_and_filters(user_input):
    """
    Analyze user input to find intents and filter criteria using ML Model
    """
    config, model, plants = _load_resources()
    norm_input = _normalize_text(user_input)
    words = norm_input.split()
    
    intent = None
    detected_filters = {}

    # 1. Detect Intent using ML
    if model:
        try:
            # Word tokenize for prediction
            tokenized_input = underthesea.word_tokenize(norm_input, format="text")
            intent = model.predict([tokenized_input])[0]
        except Exception as e:
            print(f"❌ Model Prediction Error: {e}")
            intent = 'recommendation'
    else:
        intent = 'recommendation'
        
    # Check simple intents to override if confidence was low or just explicit overrides
    # (Skip for now to rely on ML)

    # 2. Detect Entity / Filters from predefined config or ML extraction
    # Since our ML model only predicts intent, we still extract filters textually
    filter_config = config.get('filters', {})
    for field, options in filter_config.items():
        for value, keywords in options.items():
            for kw in keywords:
                if kw in norm_input:
                    detected_filters[field] = value
                    break 

    # Look for specific plant name (if intent is ask_specific_plant or recommendation)
    if (intent == 'ask_specific_plant' or intent == 'recommendation') and plants:
        for p in plants:
            # simple check
            if p['name'].lower() in norm_input:
                detected_filters['specific_plant_slug'] = p['slug']
                # If we found a specific plant, definitively set intent
                intent = 'ask_specific_plant'
                break

    return intent, detected_filters

def chatbot_response(request_message, context=None):
    """
    Main entry point for chatbot.
    request_message: str (User's text input)
    context: dict (History/session context - optional)
    """
    config, _, _ = _load_resources()
    intent, filters = _extract_intents_and_filters(request_message)
    
    # Logic Processing
    if intent == 'greeting' and not filters:
        return {
            'message': config['responses']['greeting'],
            'data': []
        }
        
    # Query Database
    products = Product.objects.filter(is_active=True)
    
    # Check specific plant
    if 'specific_plant_slug' in filters:
        products = products.filter(slug=filters['specific_plant_slug'])
        # remove it so it's not processed as dynamic Q
        del filters['specific_plant_slug']
    
    # Apply detected filters
    if filters:
        query_q = Q()
        for field, value in filters.items():
            query_q &= Q(**{field: value})
        
        products = products.filter(query_q)
        
        # Explain what we understood
        understanding = []
        if 'location_type' in filters:
            understanding.append(f"vị trí {filters['location_type']}")
        if 'care_level' in filters:
            understanding.append(f"chăm sóc {_translate_care(filters['care_level'])}")
        # ... more explanations if needed
    
    # If it was an "ask_specific_plant" intent but we didn't extract any known plant,
    # it means the user asked for a plant not in our 10 selected plants
    if intent == 'ask_specific_plant' and not filters:
         return {
            'message': "Xin lỗi, hiện tại cửa hàng mình chỉ hỗ trợ tư vấn và bán các dòng cây có trong bộ siêu tập chọn lọc. Bạn thử tham khảo các ròng cây tiểu cảnh khác nhé!",
            'data': []
        }
        
    # Get results
    results = products.order_by('-is_featured', 'price')[:5] # Top 5
    
    if not results.exists():
         return {
            'message': config['responses']['no_result'],
            'data': []
        }
    
    # Format response
    response_products = []
    for p in results:
        response_products.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'original_price': float(p.original_price) if p.original_price else None,
            'image_url': p.image.url if p.image else '',
            'url': f"/products/{p.slug}/" # Simple URL construction or use get_absolute_url if model method available in context
        })
        
    msg = f"Mình tìm thấy {len(results)} cây phù hợp với bạn:"
    if filters:
        msg = f"Theo yêu cầu của bạn, mình gợi ý:"
        
    return {
        'message': msg,
        'data': response_products,
        'filters_detected': filters 
    }

def _translate_care(val):
    """Helper to translate internal codes slightly for debug/echo"""
    if val == 'easy': return 'dễ'
    if val == 'hard': return 'khó'
    return val
