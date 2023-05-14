from . import views
from django.urls import path

urlpatterns = [
    path('settings/', views.get_settings, name='settings'),
    path('proxies/', views.get_proxies, name='proxies'),
    path('users/', views.get_users, name='users'),
    path('locations/', views.get_locations, name='locations'),
    path('streams/', views.get_streams, name='streams'),
    path('disable-user/<name>/', views.disable_user, name='disable_user'),
]