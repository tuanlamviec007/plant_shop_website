from django.db import models
from django.contrib.auth.models import User
from products.models import Product





class ChatSession(models.Model):
    """Phiên chat với AI"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)  # Dùng cho guest
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_sessions'
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat Session {self.session_id}"


class ChatMessage(models.Model):
    """Tin nhắn trong phiên chat"""
    SENDER_CHOICES = [
        ('user', 'Khách hàng'),
        ('bot', 'AI Assistant'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    
    # AI có thể gợi ý sản phẩm kèm theo
    recommended_products = models.ManyToManyField(Product, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}..."
