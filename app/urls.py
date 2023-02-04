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
    path('404/', views.error404, name='404'),
    path('logout/', views.logout, name='logout'),
    path('add-comment/', views.add_comment, name='add-comment'),
    path('refresh-token/', views.refresh_token, name='refresh-token'),
    path('points/', views.points, name='points'),
    path('schedule/', views.schedule, name='schedule'),
    path('support/', views.support, name='support'),
    path('ranking/', views.ranking, name='ranking'),
    path('profile/', views.profile, name='profile'),
    path('wallet/', views.wallet, name='wallet'),
    path('testing/', views.testing, name='testing'),
]
