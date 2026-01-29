from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .ai_service import chatbot_response

@require_POST
def chat_api(request):
    """API xử lý chat với AI"""
    try:
        data = json.loads(request.body)
        step = data.get('step', 'start')
        answer = data.get('answer')
        context = data.get('context', {})
        
        response_data = chatbot_response(step, answer, context)
        
        if 'product' in response_data:
            product = response_data['product']
            # Serialize product data manually for JSON response
            response_data['product'] = {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'image_url': product.image.url if product.image else '',
                'url': product.get_absolute_url()
            }
            
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
