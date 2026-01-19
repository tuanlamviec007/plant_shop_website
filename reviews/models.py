from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models import Avg


class Review(models.Model):
    """Đánh giá sản phẩm"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'is_approved']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Cập nhật rating trung bình của sản phẩm
        self.update_product_rating()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        # Cập nhật lại rating sau khi xóa
        reviews = Review.objects.filter(product=product, is_approved=True)
        if reviews.exists():
            product.rating_avg = reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating_count = reviews.count()
        else:
            product.rating_avg = 0
            product.rating_count = 0
        product.save()

    def update_product_rating(self):
        """Cập nhật rating trung bình của sản phẩm"""
        reviews = Review.objects.filter(product=self.product, is_approved=True)
        self.product.rating_avg = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        self.product.rating_count = reviews.count()
        self.product.save()
