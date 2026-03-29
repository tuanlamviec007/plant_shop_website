from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating_stars', 'is_approved', 'created_at', 'is_approved_status']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['user__username', 'product__name', 'comment']
    list_editable = []  # Bỏ list_editable cho is_approved để dùng method hiển thị đẹp hơn nếu muốn, hoặc giữ nguyên
    readonly_fields = ['created_at']

    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        color = '#ffc107' if obj.rating >= 4 else '#6c757d'
        return format_html('<span style="color: {}; font-size: 1.2em;">{}</span>', color, stars)
    rating_stars.short_description = 'Đánh giá'

    def is_approved_status(self, obj):
        if obj.is_approved:
            return mark_safe('<span style="color: #28a745;"><i class="fas fa-check-circle"></i> Đã duyệt</span>')
        return mark_safe('<span style="color: #dc3545;"><i class="fas fa-times-circle"></i> Đợi duyệt</span>')
    is_approved_status.short_description = 'Trạng thái'
