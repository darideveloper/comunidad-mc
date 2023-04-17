from . import models
from django.contrib import admin

@admin.register (models.User)
class AdminUser (admin.ModelAdmin):
    
    list_display = ('id', 'name', 'cookies', 'is_active')
    ordering = ('id', 'name', 'cookies', 'is_active')
    search_fields = ('cookies', 'is_active')
    list_per_page = 20
