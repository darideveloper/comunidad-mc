from . import views
from django.urls import path

urlpatterns = [
    path('donations/', views.get_donations, name='donations'),
    path('proxy/', views.get_proxy, name='proxy'),
    path('disable-user/<name>/', views.disable_user, name='disable_user'),
    path('update-donation/<int:id>/', views.upodate_donation, name='update_donation'),
    path('users/', views.get_users, name='get_users'),
    path('update-cookies/<name>/', views.update_cookies, name='get_user'),
]