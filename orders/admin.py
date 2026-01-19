from django.contrib import admin
from .models import Order, OrderItem, Cart


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'quantity', 'price', 'subtotal']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_code', 'user', 'customer_name', 'total_amount',
                    'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_code', 'customer_name', 'customer_phone', 'customer_email']
    list_editable = ['status']
    readonly_fields = ['order_code', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('order_code', 'user', 'total_amount', 'status', 'payment_method')
        }),
        ('Thông tin khách hàng', {
            'fields': ('customer_name', 'customer_phone', 'customer_email',
                       'shipping_address', 'note')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        """Khi admin cập nhật trạng thái đơn hàng"""
        if change:
            try:
                old_status = Order.objects.get(pk=obj.pk).status
                new_status = obj.status

                # Khi chuyển từ pending sang confirmed: giảm stock
                if old_status == 'pending' and new_status == 'confirmed':
                    for item in obj.items.all():
                        product = item.product
                        product.stock -= item.quantity
                        product.sold_count += item.quantity
                        product.save()

                # Khi hủy đơn: hoàn lại stock (nếu đã confirmed)
                if old_status == 'confirmed' and new_status == 'cancelled':
                    for item in obj.items.all():
                        product = item.product
                        product.stock += item.quantity
                        product.sold_count -= item.quantity
                        product.save()
            except Order.DoesNotExist:
                # Trường hợp tạo mới (nhưng Admin ít khi tạo đơn thủ công kiểu này)
                pass

        super().save_model(request, obj, form, change)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__name']
