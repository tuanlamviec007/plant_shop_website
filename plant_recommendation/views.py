from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .ai_service import chatbot_response

@require_POST
def chat_api(request):
    """API xử lý chat với AI"""
    try:
        data = json.loads(request.body)
        # Old frontend sends 'step', 'answer', 'context'. 
        # New intent: User sends a message text.
        # We can support backward compatibility or expect 'message' key.
        
        user_message = data.get('message')
        if not user_message and data.get('answer'):
             # Fallback if frontend sends 'answer' as the text
             user_message = data.get('answer')
             
        if not user_message:
            user_message = "xin chao" # Default greeting if empty
        
        context = data.get('context', {})
        
        response_data = chatbot_response(user_message, context)
        
        return JsonResponse(response_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
