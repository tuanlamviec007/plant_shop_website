from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from products.models import Product
from orders.models import OrderItem


@login_required
def add_review(request, product_id):
    """Thêm đánh giá sản phẩm"""
    product = get_object_or_404(Product, id=product_id)

    # Kiểm tra đã mua sản phẩm chưa
    user_purchased = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__status='delivered'
    ).exists()

    if not user_purchased:
        messages.error(request, 'Bạn chỉ có thể đánh giá sản phẩm đã mua!')
        return redirect('product_detail', slug=product.slug)

    # Kiểm tra đã đánh giá chưa
    if Review.objects.filter(user=request.user, product=product).exists():
        messages.warning(request, 'Bạn đã đánh giá sản phẩm này rồi!')
        return redirect('product_detail', slug=product.slug)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')

        Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment
        )

        messages.success(request, 'Cảm ơn bạn đã đánh giá!')
        return redirect('product_detail', slug=product.slug)

    return redirect('product_detail', slug=product.slug)
