"""
AI Recommendation Service - NLP Implementation
"""
import os
import json
import unicodedata
import re
from django.conf import settings
from django.db.models import Q
from products.models import Product

# Path to config file
CONFIG_PATH = os.path.join(settings.BASE_DIR, 'plant_recommendation', 'chatbot_config.json')
_config = None

def _load_config():
    """Load configuraton from JSON file"""
    global _config
    if _config is None:
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                _config = json.load(f)
        except Exception as e:
            print(f"❌ Config load error: {e}")
            # Fallback default config to prevent crash
            _config = {"intents": {}, "filters": {}}
    return _config

def _normalize_text(text):
    """Normalize text: remove accents, lowercase, remove special chars"""
    if not text:
        return ""
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def _extract_intents_and_filters(user_input):
    """
    Analyze user input to find intents and filter criteria
    """
    config = _load_config()
    norm_input = _normalize_text(user_input)
    words = norm_input.split()
    
    intent = None
    detected_filters = {}

    # 1. Detect Intent
    for int_name, keywords in config.get('intents', {}).items():
        for kw in keywords:
            # Check if keyword exists in normalized input
            # Simple check: kw in norm_input
            if kw in norm_input:
                intent = int_name
                break
        if intent:
            break
            
    # Default to recommendation if unknown but has filters, or just generic interaction
    if not intent:
        intent = 'recommendation'

    # 2. Detect Filters
    filter_config = config.get('filters', {})
    for field, options in filter_config.items():
        for value, keywords in options.items():
            for kw in keywords:
                # Use regex boundry or simple inclusion? simple inclusion for now
                if kw in norm_input:
                    detected_filters[field] = value
                    break # prioritize first match for this field
    
    return intent, detected_filters

def chatbot_response(request_message, context=None):
    """
    Main entry point for chatbot.
    request_message: str (User's text input)
    context: dict (History/session context - optional)
    """
    config = _load_config()
    intent, filters = _extract_intents_and_filters(request_message)
    
    # Logic Processing
    if intent == 'greeting' and not filters:
        return {
            'message': config['responses']['greeting'],
            'data': []
        }
        
    # Query Database
    products = Product.objects.filter(is_active=True)
    
    # Apply detected filters
    if filters:
        query_q = Q()
        for field, value in filters.items():
            # Construct dynamic Q object: field__exact=value
            query_q &= Q(**{field: value})
        
        products = products.filter(query_q)
        
        # Explain what we understood
        understanding = []
        if 'location_type' in filters:
            understanding.append(f"vị trí {filters['location_type']}")
        if 'care_level' in filters:
            understanding.append(f"chăm sóc {_translate_care(filters['care_level'])}")
        # ... more explanations if needed
    
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
