from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_recognition_view, name='ai_recognition'),
    path('recognize/', views.recognize_plant, name='recognize_plant'),
    path('history/', views.recognition_history, name='recognition_history'),
]
