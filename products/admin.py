# products/admin.py
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'sold_count',
                    'rating_avg', 'is_featured', 'is_active', 'created_at']
    list_filter = ['category', 'care_level', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_featured', 'is_active']
    readonly_fields = ['sold_count', 'rating_avg', 'rating_count', 'created_at', 'updated_at']

    list_per_page = 20
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('category', 'name', 'slug', 'description', 'image')
        }),
        ('Giá & Kho', {
            'fields': ('price', 'original_price', 'stock', 'sold_count')
        }),
        ('Chăm sóc', {
            'fields': ('care_level', 'light_requirement', 'water_frequency')
        }),
        ('Đánh giá', {
            'fields': ('rating_avg', 'rating_count')
        }),
        ('Trạng thái', {
            'fields': ('is_featured', 'is_active', 'created_at', 'updated_at')
        }),
    )

