from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Cart, Order, OrderItem
from products.models import Product


@login_required
def cart_view(request):
    """Xem giỏ hàng"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')

    # Tính tổng tiền
    total = sum(item.subtotal for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Thêm sản phẩm vào giỏ hàng"""
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # Kiểm tra tồn kho
        if quantity > product.stock:
            messages.error(request, f'Sản phẩm chỉ còn {product.stock} sản phẩm trong kho!')
            return redirect('product_detail', slug=product.slug)

        # Thêm hoặc cập nhật giỏ hàng
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                messages.error(request, f'Không đủ hàng trong kho!')
                return redirect('cart')
            cart_item.save()
            messages.success(request, f'Đã cập nhật số lượng {product.name}!')
        else:
            messages.success(request, f'Đã thêm {product.name} vào giỏ hàng!')

        return redirect('cart')

    return redirect('product_detail', slug=product.slug)


@login_required
def update_cart(request, cart_id):
    """Cập nhật số lượng trong giỏ hàng"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
        elif quantity > cart_item.product.stock:
            messages.error(request, f'Chỉ còn {cart_item.product.stock} sản phẩm trong kho!')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Đã cập nhật giỏ hàng!')

    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    return redirect('cart')


@login_required
def checkout(request):
    """Thanh toán"""
    cart_items = Cart.objects.filter(user=request.user).select_related('product')

    if not cart_items.exists():
        messages.warning(request, 'Giỏ hàng trống!')
        return redirect('cart')

    # Tính tổng tiền
    total = sum(item.subtotal for item in cart_items)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email', '')
        shipping_address = request.POST.get('shipping_address')
        note = request.POST.get('note', '')
        payment_method = request.POST.get('payment_method', 'cod')

        # Validate
        if not all([customer_name, customer_phone, shipping_address]):
            messages.error(request, 'Vui lòng điền đầy đủ thông tin!')
            return redirect('checkout')

        # Tạo đơn hàng trong transaction
        try:
            with transaction.atomic():
                # Tạo order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=total,
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    customer_email=customer_email,
                    shipping_address=shipping_address,
                    note=note,
                    payment_method=payment_method,
                    status='pending'
                )

                # Tạo order items
                for cart_item in cart_items:
                    # Kiểm tra lại tồn kho
                    if cart_item.quantity > cart_item.product.stock:
                        raise ValueError(f'Sản phẩm {cart_item.product.name} không đủ hàng!')

                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        product_name=cart_item.product.name,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )

                # Xóa giỏ hàng
                cart_items.delete()

                messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: {order.order_code}')
                return redirect('order_detail', order_id=order.id)

        except ValueError as e:
            messages.error(request, str(e))
            return redirect('cart')
        except Exception as e:
            messages.error(request, 'Có lỗi xảy ra! Vui lòng thử lại.')
            return redirect('cart')

    # Lấy thông tin user để điền sẵn
    profile = request.user.profile if hasattr(request.user, 'profile') else None

    context = {
        'cart_items': cart_items,
        'total': total,
        'profile': profile,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_list(request):
    """Danh sách đơn hàng của user"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_id):
    """Chi tiết đơn hàng"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def cancel_order(request, order_id):
    """Hủy đơn hàng (chỉ khi status = pending)"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Đã hủy đơn hàng!')
    else:
        messages.error(request, 'Không thể hủy đơn hàng này!')

    return redirect('order_detail', order_id=order.id)
