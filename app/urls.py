# mysite/urls.py
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('landing/', views.landing, name='landing'),
    path('404/', views.error404, name='404')
]
