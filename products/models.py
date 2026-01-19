# products/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """Danh mục cây cảnh"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Sản phẩm cây cảnh"""
    CARE_LEVEL_CHOICES = [
        ('easy', 'Dễ'),
        ('medium', 'Trung bình'),
        ('hard', 'Khó'),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá")
    original_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True,
                                         verbose_name="Giá gốc")
    image = models.ImageField(upload_to='products/', verbose_name="Hình ảnh")
    stock = models.IntegerField(default=0, verbose_name="Tồn kho")
    sold_count = models.IntegerField(default=0, verbose_name="Đã bán")

    # Thông tin chăm sóc
    care_level = models.CharField(max_length=20, choices=CARE_LEVEL_CHOICES, default='easy')
    light_requirement = models.CharField(max_length=100, blank=True, verbose_name="Ánh sáng")
    water_frequency = models.CharField(max_length=100, blank=True, verbose_name="Tưới nước")

    # Đánh giá
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count = models.IntegerField(default=0)

    # Trạng thái
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        """Tính % giảm giá"""
        if self.original_price and self.original_price > self.price:
            return int((1 - self.price / self.original_price) * 100)
        return 0

    @property
    def in_stock(self):
        """Kiểm tra còn hàng"""
        return self.stock > 0



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        """Tính % giảm giá"""
        if self.original_price and self.original_price > self.price:
            return int((1 - self.price / self.original_price) * 100)
        return 0

    @property
    def in_stock(self):
        """Kiểm tra còn hàng"""
        return self.stock > 0
