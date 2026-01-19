from django.contrib import admin
from .models import PlantRecognition


@admin.register(PlantRecognition)
class PlantRecognitionAdmin(admin.ModelAdmin):
    list_display = ['detected_plant_name', 'user', 'confidence',
                    'suggested_product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['detected_plant_name', 'user__username']
    readonly_fields = ['created_at']
