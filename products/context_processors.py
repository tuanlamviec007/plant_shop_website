# products/context_processors.py
# Tạo file mới này trong thư mục products/

from orders.models import Cart
from products.models import Category

def cart_count(request):
    """Context processor để hiển thị số lượng giỏ hàng ở navbar"""
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
        return {'cart_count': count}
    return {'cart_count': 0}


def categories(request):
    """Context processor để hiển thị categories ở mọi trang"""
    return {
        'all_categories': Category.objects.filter(is_active=True)
    }