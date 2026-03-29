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

def _load_resources():
    global _config, _model
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
    # Always reload plants fresh from disk so retraining is reflected immediately
    plants = []
    try:
        with open(PLANTS_PATH, 'r', encoding='utf-8-sig') as f:
            plants = json.load(f)
    except Exception:
        plants = []
    return _config, _model, plants

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

    # Detect category from input
    if 'trong phòng' in norm_input or 'trong nhà' in norm_input:
        detected_filters['category'] = 'cây để trong phòng'
    elif 'sân vườn' in norm_input or 'ngoài trời' in norm_input or 'ban công' in norm_input:
        detected_filters['category'] = 'cây trồng tại sân vườn'

    # Detect desk suitability
    if 'để bàn' in norm_input or 'bàn làm việc' in norm_input:
        detected_filters['desk_suitable'] = True 

    # Detect price conditions
    price_keywords = ['giá', 'đắt', 'rẻ', 'nhỏ hơn', 'lớn hơn', 'dưới', 'trên', 'so với', 'hơn', 'ít hơn']
    if any(kw in norm_input for kw in price_keywords):
        detected_filters['price_condition'] = {}
        # Extract numbers (assuming VND, remove commas)
        numbers = re.findall(r'\d+', user_input.replace(',', ''))  # Use original user_input for numbers
        if numbers:
            value = int(numbers[0])
            # Check in original user_input for operators
            if '<' in user_input or 'nhỏ hơn' in user_input or 'dưới' in user_input or 'ít hơn' in user_input:
                detected_filters['price_condition']['operator'] = 'lt'
                detected_filters['price_condition']['value'] = value
            elif '>' in user_input or 'lớn hơn' in user_input or 'trên' in user_input or 'hơn' in user_input:
                detected_filters['price_condition']['operator'] = 'gt'
                detected_filters['price_condition']['value'] = value
        # Check for comparison with specific plant
        for p in plants:
            if p['name'].lower() in user_input.lower():  # Check in original
                detected_filters['price_condition']['operator'] = 'lt_plant' if 'nhỏ hơn' in user_input or 'ít hơn' in user_input else 'gt_plant'
                detected_filters['price_condition']['plant_slug'] = p['slug']
                break

    # Look for specific plant name (if intent is ask_specific_plant or recommendation or ask_plant_characteristics)
    if intent in ['ask_specific_plant', 'recommendation', 'ask_plant_characteristics']:
        found_plant = None
        for p in plants:
            if p['name'].lower() in norm_input:
                found_plant = p
                if intent == 'recommendation':
                    detected_filters['search_name'] = p['name']
                else:
                    detected_filters['specific_plant_slug'] = p['slug']
                    if intent != 'ask_plant_characteristics':
                        intent = 'ask_specific_plant'
                break
        # Nếu không tìm thấy tên cây trong selected_plants thì luôn báo không có mặt hàng này
        if not found_plant:
            # Lấy tên cây người dùng hỏi (sau các từ khóa tìm, mua, xem...)
            import re
            match = re.search(r"(?:tìm|tư vấn|mua|xem|giới thiệu|bán)?(?: cho tôi| giúp)?(?: cây)? ([\w\s]+)", user_input.lower())
            if match:
                detected_filters['not_found_plant_name'] = match.group(1).strip()
            else:
                detected_filters['not_found_plant_name'] = user_input.strip()

    if intent == 'compare_plants' and plants:
        found_plants = []
        # sort plants by name length descending to match longest first (e.g. "Cây kim ngân" vs "Cây kim tiền")
        sorted_plants = sorted(plants, key=lambda x: len(x['name']), reverse=True)
        search_text = norm_input
        for p in sorted_plants:
            p_name_norm = _normalize_text(p['name'])
            # Since user might type "kim tiền" instead of "cây kim tiền", check both
            p_name_short = p_name_norm.replace('cây', '').strip()
            
            # Simple substring check is fine as long as we remove the exact substring
            # norm_input is lowercase and _normalize_text returns lowercase.
            # But just in case, use direct `in` check and `replace`
            if p_name_norm and p_name_norm in search_text:
                found_plants.append(p['slug'])
                search_text = search_text.replace(p_name_norm, ' ', 1) # replace only first occurrence
            elif p_name_short and p_name_short in search_text:
                found_plants.append(p['slug'])
                search_text = search_text.replace(p_name_short, ' ', 1)
                
        if len(found_plants) >= 2:
            detected_filters['plant_1_slug'] = found_plants[0]
            detected_filters['plant_2_slug'] = found_plants[1]
        elif len(found_plants) == 1:
            # fallback to characteristic if only 1 found
            intent = 'ask_plant_characteristics'
            detected_filters['specific_plant_slug'] = found_plants[0]

    # If it's ask_plant_characteristics, we need to know WHICH characteristic they are asking
    if intent == 'ask_plant_characteristics':
        if any(w in norm_input for w in ['tưới', 'nước']):
            detected_filters['characteristic_type'] = 'water'
        elif any(w in norm_input for w in ['chăm sóc', 'cách chăm']):
            detected_filters['characteristic_type'] = 'care'
        elif any(w in norm_input for w in ['phong thủy', 'mệnh', 'hợp']):
            detected_filters['characteristic_type'] = 'feng_shui'
        elif any(w in norm_input for w in ['sáng', 'nắng']):
            detected_filters['characteristic_type'] = 'light'
        elif any(w in norm_input for w in ['độc', 'có độc']):
            detected_filters['characteristic_type'] = 'toxicity'
        elif any(w in norm_input for w in ['tác dụng']):
            detected_filters['characteristic_type'] = 'benefits'
        elif any(w in norm_input for w in ['phân']):
            detected_filters['characteristic_type'] = 'fertilizer'
        elif any(w in norm_input for w in ['nhiệt độ']):
            detected_filters['characteristic_type'] = 'temperature'
        elif any(w in norm_input for w in ['trong nhà']):
            detected_filters['characteristic_type'] = 'indoor'
        elif any(w in norm_input for w in ['thay chậu']):
            detected_filters['characteristic_type'] = 'repotting'
        else:
            detected_filters['characteristic_type'] = 'general'

    return intent, detected_filters

def chatbot_response(request_message, context=None):
    """
    Main entry point for chatbot.
    request_message: str (User's text input)
    context: dict (History/session context - optional)
    """
    config, _, plants = _load_resources()
    intent, filters = _extract_intents_and_filters(request_message)
    
    # Nếu phát hiện hỏi về cây không có trong danh sách train thì trả về luôn thông báo không có mặt hàng này
    not_found_plant_name = filters.pop('not_found_plant_name', None)
    if not_found_plant_name:
        return {
            'message': f"Xin lỗi, hiện tại cửa hàng mình không có mặt hàng '{not_found_plant_name.strip()}'. Bạn thử tham khảo các dòng cây tiểu cảnh khác nhé!",
            'data': []
        }

    # Override intent if price condition is detected (treat as recommendation)
    if 'price_condition' in filters:
        intent = 'recommendation'

    # If desk_suitable is set, remove location_type filter since desk plants are indoor
    if 'desk_suitable' in filters:
        filters.pop('location_type', None)

    # Filter plants by category if specified
    category = filters.pop('category', None)
    if category:
        plants = [p for p in plants if p.get('category') == category]

    # Filter by desk suitability
    desk_suitable = filters.pop('desk_suitable', None)
    if desk_suitable is not None:
        plants = [p for p in plants if p.get('desk_suitable', True) == desk_suitable]
    
    # Logic Processing
    if intent == 'greeting' and not filters:
        return {
            'message': config['responses']['greeting'],
            'data': []
        }
        
    # Extract special keys before applying ORM filters
    plant_slug = filters.pop('specific_plant_slug', None)
    char_type = filters.pop('characteristic_type', 'general')
    p1_slug = filters.pop('plant_1_slug', None)
    p2_slug = filters.pop('plant_2_slug', None)
    
    # If price condition is set for recommendation, don't filter by specific plant
    if 'price_condition' in filters and intent == 'recommendation':
        plant_slug = None
    
    # Get the 10 selected plant IDs to restrict all queries to the curated list
    selected_ids = [p['id'] for p in plants] if plants else []
    
    # Query Database - always restrict to the selected plants
    products = Product.objects.filter(is_active=True)
    products = products.filter(id__in=selected_ids)
    
    # Apply price condition if detected
    price_condition = filters.pop('price_condition', None)
    if price_condition:
        if 'value' in price_condition:
            if price_condition['operator'] == 'lt':
                products = products.filter(price__lt=price_condition['value'])
            elif price_condition['operator'] == 'gt':
                products = products.filter(price__gt=price_condition['value'])
        elif 'plant_slug' in price_condition:
            try:
                ref_plant = Product.objects.get(slug=price_condition['plant_slug'], is_active=True)
                if price_condition['operator'] == 'lt_plant':
                    products = products.filter(price__lt=ref_plant.price)
                elif price_condition['operator'] == 'gt_plant':
                    products = products.filter(price__gt=ref_plant.price)
            except Product.DoesNotExist:
                pass  # ignore if plant not found
    
    if plant_slug and not ('price_condition' in filters and intent == 'recommendation'):
        products = products.filter(slug=plant_slug)
    
    # Tìm kiếm theo tên (khi intent là recommendation hoặc bất kỳ intent nào nhưng có tên cây cụ thể)
    search_name = filters.pop('search_name', None)
    if search_name:
        products = products.filter(name__icontains=search_name.replace('cây ', '').replace('Cây ', '').strip())
        if not products.exists():
            return {
                'message': f"Xin lỗi, hiện tại cửa hàng mình không tìm thấy loại cây '{search_name}' trong bộ sưu tập. Bạn thử tham khảo các dòng cây tiểu cảnh khác nhé!",
                'data': []
            }
    
    # Apply detected filters
    if filters:
        query_q = Q()
        for field, value in filters.items():
            if field == 'location_type':
                if value == 'outdoor':
                    query_q &= Q(location_type__in=['outdoor', 'both'])
                elif value == 'indoor':
                    query_q &= Q(location_type__in=['indoor', 'both'])
                else:
                    query_q &= Q(location_type=value)
            elif field in ['care_level', 'space_required', 'light_condition']:
                query_q &= Q(**{field: value})
        filtered_products = products.filter(query_q)
        if filtered_products.exists():
            products = filtered_products
        # else: keep 'products' as the full curated list if no match found
    
    # Special case for Feng Shui general query
    if intent == 'ask_plant_characteristics' and char_type == 'feng_shui' and not plant_slug:
        # User asked "cây phong thủy nào tốt", find all plants with feng_shui_meaning
        feng_shui_products = products.exclude(feng_shui_meaning__isnull=True).exclude(feng_shui_meaning__exact='')
        if feng_shui_products.exists():
            products = feng_shui_products
        
    # If it was an "ask_specific_plant" intent but we didn't extract any known plant,
    if intent in ['ask_specific_plant', 'ask_plant_characteristics'] and not plant_slug and not filters:
         return {
            'message': "Xin lỗi, hiện tại cửa hàng mình chỉ hỗ trợ tư vấn và bán các dòng cây có trong bộ sưu tập chọn lọc. Bạn thử tham khảo các dòng cây tiểu cảnh khác nhé!",
            'data': []
        }

        
    # Handle ask_plant_characteristics
    if intent == 'ask_plant_characteristics':
        # Ưu tiên lấy thông tin từ selected_plants.json nếu có
        plant_info = next((p for p in plants if p['slug'] == plant_slug), None)
        if plant_info:
            ans = ""
            # Ưu tiên trả về cách chăm sóc nếu người dùng hỏi về chăm sóc
            if any(kw in request_message.lower() for kw in ['chăm sóc', 'cách chăm', 'cach cham', 'hướng dẫn chăm', 'huong dan cham']):
                ans += f"Cách chăm sóc {plant_info['name']}: {plant_info.get('care', 'Chưa có thông tin chăm sóc.')}\n"
            if any(kw in request_message.lower() for kw in ['đặc điểm', 'dac diem', 'đặc tính', 'dac tinh']):
                ans += f"Đặc điểm của {plant_info['name']}: {plant_info.get('characteristics', 'Chưa có thông tin đặc điểm.')}\n"
            if any(kw in request_message.lower() for kw in ['ý nghĩa', 'y nghia', 'phong thủy', 'phong thuy']):
                ans += f"Ý nghĩa của {plant_info['name']}: {plant_info.get('meaning', 'Chưa có thông tin ý nghĩa.')}\n"
            if not ans:
                # fallback nếu không hỏi rõ đặc điểm, ý nghĩa hay chăm sóc
                ans = f"{plant_info['name']} là một loại cây rất tuyệt vời! Đặc điểm: {plant_info.get('characteristics', '')} Ý nghĩa: {plant_info.get('meaning', '')} Cách chăm sóc: {plant_info.get('care', '')}"
            filters['characteristic_type'] = char_type
            filters['specific_plant_slug'] = plant_slug
            return {
                'message': ans.strip(),
                'data': [],
                'filters_detected': filters
            }
        # Nếu không có trong selected_plants.json thì fallback về Product
        try:
            plant = Product.objects.get(slug=plant_slug, is_active=True)
            if char_type == 'water':
                ans = f"Đối với {plant.name}, chế độ tưới nước là: {plant.water_frequency}."
                if plant.care_tips: ans += f" Lưu ý thêm: {plant.care_tips}"
            elif char_type == 'care':
                ans = f"Chăm sóc {plant.name} thuộc mức độ {plant.get_care_level_display().lower()}."
                if plant.care_tips: ans += f" Hướng dẫn: {plant.care_tips}"
            elif char_type == 'feng_shui':
                ans = f"Về phong thủy, {plant.name} có ý nghĩa: '{plant.feng_shui_meaning}'." if plant.feng_shui_meaning else f"Hiện tại mình chưa có thông tin phong thủy chi tiết cho {plant.name}."
            elif char_type == 'light':
                ans = f"{plant.name} cần điều kiện ánh sáng như sau: {plant.light_requirement}."
            elif char_type == 'toxicity':
                ans = f"Đa số cây cảnh trong nhà đều cần cẩn trọng để xa tầm tay trẻ em và thú cưng. Bạn nên lưu ý khi chọn {plant.name} nhé!"
            elif char_type == 'benefits':
                ans = f"{plant.name} không chỉ giúp trang trí không gian mà còn mang lại sinh khí tốt, giúp lọc không khí rất hiệu quả."
            elif char_type == 'fertilizer':
                ans = f"Bạn nên bón phân định kỳ cho {plant.name} khoảng 1-2 tháng/lần để cây xanh tốt nhất."
            elif char_type == 'temperature':
                ans = f"{plant.name} thường phát triển tốt nhất ở nhiệt độ phòng (khoảng 18-28 độ C)."
            elif char_type == 'indoor':
                ans = f"{plant.name} { 'rất phù hợp' if plant.location_type in ['indoor', 'both'] else 'không thực sự phù hợp' } để trồng trong nhà."
            elif char_type == 'repotting':
                ans = f"Bạn nên thay chậu cho {plant.name} mỗi 1-2 năm hoặc khi thấy rễ cây phát triển chật kín chậu."
            else:
                ans = f"{plant.name} Đặc điểm: {plant.description[:200]}..."
            filters['characteristic_type'] = char_type
            filters['specific_plant_slug'] = plant_slug
            return {
                'message': ans,
                'data': [],
                'filters_detected': filters
            }
        except Product.DoesNotExist:
            return {
                'message': "Mình không tìm thấy thông tin chi tiết về cây bạn hỏi.",
                'data': []
            }
            
    # Handle compare_plants
    if intent == 'compare_plants':
        p1_slug = filters.pop('plant_1_slug', None)
        p2_slug = filters.pop('plant_2_slug', None)
        if p1_slug and p2_slug:
            try:
                p1 = Product.objects.get(slug=p1_slug)
                p2 = Product.objects.get(slug=p2_slug)
                ans = f"So sánh {p1.name} và {p2.name}:\n"
                ans += f"- **{p1.name}**: Có giá {p1.price}đ. Mức độ chăm sóc: {p1.get_care_level_display()}.\n"
                ans += f"- **{p2.name}**: Có giá {p2.price}đ. Mức độ chăm sóc: {p2.get_care_level_display()}.\n"
                if p1.care_level == p2.care_level:
                    ans += f"Hai cây này đều có mức độ chăm sóc '{p1.get_care_level_display().lower()}' nên tùy thuộc vào không gian và sở thích để bạn chọn nhé!"
                else:
                    easier = p1 if (p1.care_level == 'easy' or (p1.care_level == 'medium' and p2.care_level == 'hard')) else p2
                    ans += f"Nói chung, {easier.name} sẽ là lựa chọn dễ chăm hơn cho bạn."
                
                return {
                    'message': ans,
                    'data': [
                        {'id': p1.id, 'name': p1.name, 'price': float(p1.price), 'image_url': p1.image.url if p1.image else '', 'url': f"/products/{p1.slug}/"},
                        {'id': p2.id, 'name': p2.name, 'price': float(p2.price), 'image_url': p2.image.url if p2.image else '', 'url': f"/products/{p2.slug}/"}
                    ],
                    'filters_detected': filters
                }
            except Product.DoesNotExist:
                return {
                 'message': "Xin cám ơn, nhưng mình chưa có đủ thông tin để so sánh 2 cây đó trong bộ sưu tập bạn nhé.",
                 'data': []
             }
        else:
             return {
                 'message': "Mình hiểu bạn muốn so sánh cây, nhưng bạn vui lòng cho mình biết rõ tên 2 loại cây cần so sánh (ví dụ: so sánh cây kim tiền và lan ý) nhé!",
                 'data': []
             }
        
    # Get results
    results = products.order_by('price')[:5] # Top 5

    if len(results) == 0:
        return {
            'message': "Xin lỗi, hiện tại cửa hàng mình không tìm thấy loại cây bạn yêu cầu trong bộ sưu tập. Bạn thử tham khảo các dòng cây tiểu cảnh khác nhé!",
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
