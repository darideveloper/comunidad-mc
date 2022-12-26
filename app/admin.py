from . import models 
from django.contrib import admin

@admin.register (models.User)
class AdminUser (admin.ModelAdmin):
    
    change_form_template = 'admin/change_form_users.html'
    
    list_display = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('country', 'time_zone')
    ordering = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone', 'country', 'time_zone')
    search_help_text = "Buscar usuarios por nombre, apellido, email, país o zona horaria"
    