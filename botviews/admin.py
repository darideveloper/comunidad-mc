from . import models
from django.contrib import admin
from app import tools, models as app_models

@admin.register (models.User)
class AdminUser (admin.ModelAdmin):
    
    list_display = ('id', 'name', 'last_update', 'is_active')
    list_filter = ('is_active', 'last_update')
    ordering = ('id', 'name', 'cookies', 'last_update', 'is_active')
    search_fields = ('cookies', 'is_active')
    list_per_page = 20
    
@admin.register (models.Proxy)
class AdminProxy (admin.ModelAdmin):
    
    list_display = ('id', 'host', 'port')
    ordering = ('id', 'host', 'port')
    search_fields = ('host', 'port')
    list_per_page = 20
    
@admin.register (models.Setting)
class AdminSettings (admin.ModelAdmin):
    
    list_display = ('name', 'value')
    ordering = ('name', 'value')
    search_fields = ('name', 'value')
    list_per_page = 20
    
@admin.register (models.Token)
class AdminToken (admin.ModelAdmin):
    
    list_display = ('name', 'value', 'is_active')
    list_filter = ('is_active',)
    ordering = ('name', 'value', 'is_active')
    search_fields = ('name', 'value',)
    list_per_page = 20