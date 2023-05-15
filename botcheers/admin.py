from . import models
from app import tools
from django.contrib import admin, messages
from django.core.exceptions import ValidationError


@admin.register (models.User)
class AdminUser (admin.ModelAdmin):
        
    list_display = ('id', 'name', 'last_update', 'is_active', 'user_auth')
    list_filter = ('is_active', 'last_update', 'user_auth__username')
    ordering = ('id', 'name', 'cookies', 'last_update', 'is_active', 'user_auth')
    search_fields = ('name', 'cookies', 'is_active', 'user_auth')
    list_per_page = 20

@admin.register (models.Donation)
class AdminDonation (admin.ModelAdmin):
    
    list_display = ('id', 'user',  'stream_chat_link', 'hour', 'minute', 'amount', 'message', 'done')
    list_filter = ('done', 'user', 'user__user_auth')
    ordering = ('-id', 'user', 'stream_chat_link', 'hour', 'minute', 'amount', 'message', 'done')
    search_fields = ('user', 'stream_chat_link', 'message')
    list_per_page = 20

@admin.register (models.Token)
class AdminToken (admin.ModelAdmin):
    
    list_display = ('name', 'value', 'is_active')
    list_filter = ('is_active',)
    ordering = ('name', 'value', 'is_active')
    search_fields = ('name', 'value',)
    list_per_page = 20