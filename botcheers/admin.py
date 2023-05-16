import django
from . import models
from django import forms
from django.contrib import admin

def get_admin_group (user_auth:django.contrib.auth.models.User) -> list:
    """ Get names of groups of admins

    Args:
        user_auth (django.contrib.auth.models.User): django user
        
    Returns:
        list: group names
    """
    
    group_names = []
    for group in user_auth.groups.all():
        group_names.append (group.name)
    return group_names
    

@admin.register (models.User)
class AdminUser (admin.ModelAdmin):
        
    list_display = ('id', 'name', 'last_update', 'is_active', 'user_auth')
    list_filter = ('is_active', 'last_update', 'user_auth__username')
    ordering = ('id', 'name', 'cookies', 'last_update', 'is_active', 'user_auth')
    search_fields = ('name', 'cookies', 'is_active', 'user_auth')
    list_per_page = 20
    
    def get_form (self, request, object, **kwargs):
        """ Filter query set of 'user' field """
        
        # Get form
        form = super(AdminUser, self).get_form(request, object, **kwargs)
        
        # Limit users to the regular bot cheers managers
        admin_groups = get_admin_group (request.user)
        if "bot cheers manager regular" in admin_groups:
            form.base_fields["user_auth"].initial  = request.user.id
            form.base_fields["user_auth"].disabled = True
            form.base_fields["user_auth"].widget = forms.HiddenInput()
            
        return form

    def get_queryset(self, request):
        
        # Get admin type
        user_auth = request.user
        admin_groups = get_admin_group (request.user)

        if "bot cheers manager" in admin_groups:
            
            # Render only donations of the current user
            return models.User.objects.filter(user_auth=user_auth)
            
        # Render all streams
        return models.User.objects.all()     

@admin.register (models.Donation)
class AdminDonation (admin.ModelAdmin):
    
    list_display = ('id', 'user',  'stream_chat_link', 'hour', 'minute', 'amount', 'message', 'done')
    list_filter = ('done', 'user', 'user__user_auth')
    ordering = ('-id', 'user', 'stream_chat_link', 'hour', 'minute', 'amount', 'message', 'done')
    search_fields = ('user', 'stream_chat_link', 'message')
    list_per_page = 20
    
    def get_form (self, request, object, **kwargs):
        """ Filter query set of 'user' field """
        
        # Get form
        form = super(AdminDonation, self).get_form(request, object, **kwargs)
        
        # Limit users to the regular bot cheers managers
        admin_groups = get_admin_group (request.user)
        if "bot cheers manager regular" in admin_groups:
            form.base_fields["user"].queryset = models.User.objects.filter(user_auth=request.user)
            
        return form

    def get_queryset(self, request):
        
        # Get admin type
        user_auth = request.user
        admin_groups = get_admin_group (request.user)

        if "bot cheers manager" in admin_groups:
            
            # Get all users of the current admin
            users = models.User.objects.filter(user_auth=user_auth)
            
            # Render only donations of the current user
            return models.Donation.objects.filter(user__in=users)
            
        # Render all streams
        return models.Donation.objects.all()     

@admin.register (models.Token)
class AdminToken (admin.ModelAdmin):
    
    list_display = ('name', 'value', 'is_active')
    list_filter = ('is_active',)
    ordering = ('name', 'value', 'is_active')
    search_fields = ('name', 'value',)
    list_per_page = 20
    
   