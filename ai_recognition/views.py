from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PlantRecognition
from products.models import Product
import random

def ai_recognition_view(request):
    """Trang upload ảnh để nhận diện"""
    return render(request, 'ai_recognition/upload.html')

def recognize_plant(request):
    """Xử lý nhận diện cây (Giả lập)"""
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # 1. Tìm một sản phẩm ngẫu nhiên để làm kết quả
        # Trong thực tế sẽ gọi API AI ở đây
        all_products = Product.objects.filter(is_active=True)
        if not all_products.exists():
            messages.error(request, 'Chưa có dữ liệu cây trong hệ thống!')
            return redirect('ai_recognition')
            
        suggested_product = random.choice(all_products)
        confidence = random.uniform(85.0, 99.9)
        
        # 2. Lưu lịch sử
        recognition = PlantRecognition.objects.create(
            user=request.user if request.user.is_authenticated else None,
            image=image,
            detected_plant_name=suggested_product.name,
            confidence=confidence,
            suggested_product=suggested_product,
            ai_response='{"simulated": true}'
        )
        
        # 3. Chuyển hướng đến trang kết quả (hoặc chi tiết sản phẩm)
        messages.success(request, f'AI đã nhận diện được cây: {suggested_product.name} ({confidence:.1f}%)')
        return redirect('product_detail', slug=suggested_product.slug)
        
    return redirect('ai_recognition')

@login_required
def recognition_history(request):
    """Lịch sử nhận diện của user"""
    history = PlantRecognition.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ai_recognition/history.html', {'history': history})
