import django
from . import models
from app import tools
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
    
    # Template for customize change form
    change_form_template = 'admin/change_form_cheers_bots.html' 
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """ auto set current user as user_auth """
        
        # get bots ids
        user_auth = request.user
        admin_groups = get_admin_group (request.user)
        
        # Format data
        extra_context = {"admin_groups": admin_groups, "user_auth_id": user_auth.id}
        
        # Render change view and submit data
        return super(AdminUser, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
        
    def add_view(self, request, form_url='', extra_context=None):
        """ auto set current user as user_auth """
        
        # get bots ids
        user_auth = request.user
        admin_groups = get_admin_group (request.user)
        
        # Format data
        extra_context = {"admin_groups": admin_groups, "user_auth_id": user_auth.id}
        
        # Render change view and submit data
        return super(AdminUser, self).add_view(
            request, form_url, extra_context=extra_context,
        )

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
    
    # Template for customize change form
    change_form_template = 'admin/change_form_donations.html' 
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """ show only user bots in change view """
        
        # get bots ids
        user_auth = request.user
        admin_groups = get_admin_group (request.user)
        users = models.User.objects.filter(user_auth=user_auth)
        users_ids = [user.id for user in users]
        
        # Format data
        extra_context = {"admin_groups": admin_groups, "users_ids": users_ids}
        
        # Render change view and submit data
        return super(AdminDonation, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
        
    def add_view(self, request, form_url='', extra_context=None):
        """ render change form template for deactive fields for platinum admins """
        
        # get bots ids
        user_auth = request.user
        admin_groups = get_admin_group (request.user)
        users = models.User.objects.filter(user_auth=user_auth)
        users_ids = [user.id for user in users]
        
        # Format data
        extra_context = {"admin_groups": admin_groups, "users_ids": users_ids}
        
        # Render change view and submit data
        return super(AdminDonation, self).add_view(
            request, form_url, extra_context=extra_context,
        )

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
    
   