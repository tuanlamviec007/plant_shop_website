from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PlantRecognition
from products.models import Product
from .ai_service import identify_plant
import random

def ai_recognition_view(request):
    """Trang upload ảnh để nhận diện"""
    return render(request, 'ai_recognition/upload.html')

@login_required
def recognize_plant(request):
    """Xử lý nhận diện cây (Sử dụng PlantNet API)"""
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # 1. Lưu tạm ảnh để gửi đi hoặc lưu thẳng vào model (ở đây lưu vào model trước để có path)
        # Ta sẽ tạo record trước, sau đó update kết quả
        recognition = PlantRecognition.objects.create(
            user=request.user,
            image=image
        )
        
        # Lấy đường dẫn file ảnh
        image_path = recognition.image.path
        
        # 2. Gọi AI Service
        try:
            result = identify_plant(image_path)
            
            if result:
                detected_name = result['name']
                confidence = result['score']
                common_names = result['common_names']
                
                # 3. Tìm sản phẩm trong DB (So khớp tên)
                # Tìm chính xác hoặc chứa tên
                # Ưu tiên tìm chính xác
                suggested_product = Product.objects.filter(name__icontains=detected_name).first()
                
                # Nếu không thấy, thử tìm theo common names
                if not suggested_product and common_names:
                    for name in common_names:
                        suggested_product = Product.objects.filter(name__icontains=name).first()
                        if suggested_product:
                            break
                
                # Cập nhật record
                recognition.detected_plant_name = detected_name
                recognition.confidence = confidence
                recognition.suggested_product = suggested_product
                recognition.ai_response = result['raw_data']
                recognition.save()
                
                messages.success(request, f'AI đã nhận diện được cây: {detected_name} ({confidence:.1f}%)')
                
                if suggested_product:
                    return redirect('product_detail', slug=suggested_product.slug)
                else:
                    # Nếu không tìm thấy sản phẩm bán, vẫn hiển thị lịch sử hoặc trang kết quả chung
                    # Hiện tại redirect về history để xem kết quả
                    messages.info(request, "Chúng tôi chưa bán loại cây này, nhưng đã lưu kết quả.")
                    return redirect('recognition_history')
            else:
                messages.error(request, 'Không thể nhận diện cây trong ảnh. Vui lòng thử ảnh khác rõ nét hơn.')
                recognition.delete() # Xóa record rác nếu lỗi
                
        except Exception as e:
            messages.error(request, f'Lỗi hệ thống: {str(e)}')
            recognition.delete()
            
    return redirect('ai_recognition')

@login_required
def recognition_history(request):
    """Lịch sử nhận diện của user"""
    history = PlantRecognition.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ai_recognition/history.html', {'history': history})

