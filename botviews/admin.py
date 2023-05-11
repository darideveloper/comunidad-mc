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
    
    list_display = ('id', 'host', 'port', 'user', 'password', 'location')
    list_filter = ('location__name', 'host')
    ordering = ('id', 'host', 'port', 'user', 'password', 'location')
    search_fields = ('host', 'port', 'user', 'password', 'location__name')
    list_per_page = 20

@admin.register (models.Location)
class AdminLocations (admin.ModelAdmin):
    
    list_display = ('id', 'name')
    ordering = ('id', 'name')
    search_fields = ('name',)
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
    
@admin.register (models.Donation)
class AdminDonation (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'stream', 'minute', 'amount', 'message', 'status')
    list_filter = ('status', 'user')
    ordering = ('-id', 'user', 'stream', 'minute', 'amount', 'message', 'status')
    search_fields = ('user', 'stream', 'message')
    list_per_page = 20
    raw_id_fields = ('stream',)
    
    def get_queryset(self, request):
        
        # Get admin type
        user_auth = request.user
        admin_type = tools.get_admin_type(user_auth=user_auth)

        if admin_type == "admin platino":
            # Get all users of the current admin
            users = app_models.User.objects.filter(user_auth=user_auth)
            
            # Render only streams of the current user
            return models.Donation.objects.filter(stream__user__in=users)
            
        # Render all streams
        return models.Donation.objects.all()   
