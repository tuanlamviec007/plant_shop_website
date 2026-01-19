# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Product, Category
from orders.models import Cart
from reviews.models import Review


def home(request):
    """Trang chủ"""
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(
        is_featured=True,
        is_active=True
    ).order_by('-created_at')[:8]

    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'home.html', context)


def product_list(request):
    """Danh sách sản phẩm với tìm kiếm, lọc, sắp xếp"""
    products = Product.objects.filter(is_active=True)

    # Tìm kiếm
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Lọc theo danh mục
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Lọc theo độ khó chăm sóc
    care_level = request.GET.get('care')
    if care_level:
        products = products.filter(care_level=care_level)

    # Lọc theo giá
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sắp xếp
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)

    # Phân trang
    paginator = Paginator(products, 12)  # 12 sản phẩm/trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(is_active=True)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_care': care_level,
        'sort_by': sort_by,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Sản phẩm liên quan (cùng danh mục)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    # Đánh giá
    reviews = Review.objects.filter(
        product=product,
        is_approved=True
    ).order_by('-created_at')[:10]

    # Kiểm tra user đã mua sản phẩm chưa (để cho phép đánh giá)
    user_purchased = False
    if request.user.is_authenticated:
        from orders.models import Order, OrderItem
        user_purchased = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='delivered'
        ).exists()

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'user_purchased': user_purchased,
    }
    return render(request, 'products/product_detail.html', context)



    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'user_purchased': user_purchased,
    }
    return render(request, 'products/product_detail.html', context)
