from . import views
from django.urls import path

urlpatterns = [
    path('donations/', views.get_donations, name='donations'),
]