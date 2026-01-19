from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Mở rộng thông tin User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Hồ sơ người dùng'
        verbose_name_plural = 'Hồ sơ người dùng'

    def __str__(self):
        return self.user.username
