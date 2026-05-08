import json
import traceback
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .ai_service import chatbot_response

@require_POST
def chat_api(request):
    """API xử lý chat với AI (Gemini)"""
    try:
        data = json.loads(request.body)
        
        user_message = data.get('message')
        if not user_message and data.get('answer'):
             user_message = data.get('answer')
             
        if not user_message:
            user_message = "Xin chào"
            
        # Lấy lịch sử chat từ session
        chat_history = request.session.get('chat_history', [])
        
        # Gọi AI service
        response_data = chatbot_response(user_message, chat_history)
        
        # Cập nhật lịch sử
        if 'updated_history' in response_data:
            request.session['chat_history'] = response_data['updated_history']
            del response_data['updated_history']
            request.session.modified = True
            
        return JsonResponse(response_data)
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
