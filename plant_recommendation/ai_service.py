"""
AI Recommendation Service - Decision Tree Chatbot
"""
import os

import pandas as pd
from django.conf import settings
from products.models import Product

# Load Data (Lazy loading)
CSV_PATH = os.path.join(settings.BASE_DIR, 'data', 'plants_10_limited.csv')
_df = None

def _load_data():
    global _df
    if _df is None:
        try:
            _df = pd.read_csv(CSV_PATH)
            # Normalize data for easier matching
            _df['light'] = _df['light'].str.lower().str.strip()
            _df['location'] = _df['location'].str.lower().str.strip()
            _df['care'] = _df['care'].str.lower().str.strip()
        except Exception as e:
            print(f"❌ Data load error: {e}")
            return False
    return True

def predict_plant(preferences):
    """
    Dự đoán cây phù hợp (Logic lọc tương đương Decision Tree)
    """
    if not _load_data():
        return None

    try:
        # Filter logic
        # 1. Exact Match
        matches = _df[
            (_df['light'] == preferences['light']) &
            (_df['care'] == preferences['care']) &
            ((_df['location'] == preferences['location']) | (_df['location'] == 'both'))
        ]
        
        # 2. Relaxed Match (nếu không tìm thấy chính xác)
        if matches.empty:
             matches = _df[
                (_df['location'] == preferences['location']) | (_df['location'] == 'both')
            ]
        
        if matches.empty:
             # Fallback to any plant
             plant_name_key = _df.iloc[0]['name']
        else:
             plant_name_key = matches.iloc[0]['name']
        
        # Find Product in DB
        product = Product.objects.filter(name__icontains=plant_name_key).first()
        
        reason = (
            f"Dựa trên lựa chọn: {preferences['location']}, {preferences['light']} sáng, {preferences['care']} chăm sóc.\n"
            f"AI đề xuất: {plant_name_key}"
        )

        return {
            'plant_name': plant_name_key,
            'product': product,
            'reason': reason
        }

    except Exception as e:
        print(f"Prediction Error: {e}")
        return None



def chatbot_response(step, user_answer=None, context=None):
    """
    Xử lý logic hội thoại theo luồng Decision Tree
    
    Returns:
        dict: {
            'message': str,
            'options': list, # [{'text': 'Trong nhà', 'value': 'indoor'}]
            'next_step': str or None,
            'result': dict (optional)
        }
    """
    context = context or {}
    
    # Kịch bản hội thoại
    if step == 'start':
        return {
            'message': "Chào bạn! Tôi là trợ lý AI tìm cây cảnh. Để bắt đầu, hãy cho biết bạn định đặt cây ở đâu?",
            'options': [
                {'text': 'Trong nhà', 'value': 'indoor'},
                {'text': 'Ngoài trời', 'value': 'outdoor'},
                {'text': 'Cả hai', 'value': 'both'}
            ],
            'next_step': 'ask_light'
        }
    
    elif step == 'ask_light':
        context['location'] = user_answer
        return {
            'message': "Tuyệt! Còn điều kiện ánh sáng chỗ đó thế nào?",
            'options': [
                {'text': 'Nhiều nắng', 'value': 'high'},
                {'text': 'Vừa phải', 'value': 'medium'},
                {'text': 'Ít nắng / Bóng râm', 'value': 'low'}, # Mapping low/shade in dataset -> low for simplicity
                {'text': 'Rất ít (Chỉ đèn điện)', 'value': 'shade'} 
            ],
            'next_step': 'ask_care'
        }
        
    elif step == 'ask_care':
        context['light'] = user_answer
        return {
            'message': "Câu hỏi cuối nhé: Bạn có nhiều thời gian chăm sóc cây không?",
            'options': [
                {'text': 'Rất ít (Bận rộn)', 'value': 'low'},
                {'text': 'Thỉnh thoảng', 'value': 'medium'},
                {'text': 'Nhiều (Yêu chăm cây)', 'value': 'high'}
            ],
            'next_step': 'result'
        }
        
    elif step == 'result':
        context['care'] = user_answer
        
        # Normalize input if needed (dataset uses 'shade' and 'low')
        # If user selected 'shade', keep it. If 'low', keep it.
        
        result = predict_plant(context)
        
        if result and result['product']:
            msg = f"Xong! {result['reason']}"
            return {
                'message': msg,
                'options': [
                    {'text': 'Tìm cây khác', 'value': 'restart'},
                    {'text': 'Xem chi tiết', 'value': 'view_product', 'url': result['product'].get_absolute_url()}
                ],
                'next_step': 'finish',
                'product': result['product']
            }
        else:
            # Fallback nếu model fail hoặc ko tìm thấy cây
            return {
                'message': "Xin lỗi, hiện tại tôi chưa tìm thấy cây nào khớp hoàn toàn với tiêu chí này trong bộ dữ liệu 10 cây mẫu. Bạn thử thay đổi tiêu chí nhé!",
                'options': [{'text': 'Thử lại', 'value': 'restart'}],
                'next_step': 'start'
            }
            
    return {'message': "Lỗi hệ thống.", 'next_step': 'start'}
