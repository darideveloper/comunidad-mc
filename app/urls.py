# mysite/urls.py
from . import views
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Comunidad MC"
admin.site.site_title = 'Comunidad MC'
admin.site.site_url = '/'
admin.site.index_title = "Admin"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('landing/', views.landing, name='landing'),
    path('404/', views.error404, name='404')
]
