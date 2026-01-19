from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    """Đơn hàng"""
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_code = models.CharField(max_length=20, unique=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Thông tin giao hàng
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(blank=True)
    shipping_address = models.TextField()
    note = models.TextField(blank=True)

    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='cod')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['order_code']),
        ]

    def __str__(self):
        return f"#{self.order_code}"

    def save(self, *args, **kwargs):
        if not self.order_code:
            # Tạo mã đơn hàng: ORD20240118001
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            # Fix logic to avoid circular issues or complex queries on first save if needed
            # For simplicity, we just check existing orders
            last_order = Order.objects.filter(order_code__startswith=f'ORD{date_str}').order_by('-order_code').first()
            if last_order:
                try:
                    last_num = int(last_order.order_code[-3:])
                    new_num = last_num + 1
                except ValueError:
                    new_num = 1
            else:
                new_num = 1
            self.order_code = f'ORD{date_str}{new_num:03d}'
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Chi tiết đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)  # Lưu tên tại thời điểm đặt
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)  # Giá tại thời điểm đặt
    subtotal = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Chi tiết đơn hàng'
        verbose_name_plural = 'Chi tiết đơn hàng'

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


class Cart(models.Model):
    """Giỏ hàng"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    @property
    def subtotal(self):
        return self.quantity * self.product.price
