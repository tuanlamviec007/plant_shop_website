"""
URL configuration for plant_shop project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),
    path('reviews/', include('reviews.urls')),
    path('recommendation/', include('plant_recommendation.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
