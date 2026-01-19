from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class PlantRecognition(models.Model):
    """Lịch sử nhận diện cây bằng AI"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='plant_recognitions')
    image = models.ImageField(upload_to='plants/')
    detected_plant_name = models.CharField(max_length=200, blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    suggested_product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                          null=True, blank=True)
    ai_response = models.TextField(blank=True)  # Lưu JSON response
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'plant_recognitions'
        verbose_name = 'Nhận diện cây'
        verbose_name_plural = 'Nhận diện cây'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.detected_plant_name or 'Unknown'} - {self.created_at}"
