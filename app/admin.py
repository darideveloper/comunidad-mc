from . import models 
from django.contrib import admin
from . import tools

# Filter classes
class FilterWeeklyDailyPoints (admin.SimpleListFilter):
    """ Filter points by user name """
    
    # Visible texts
    title = 'Usuario con puntos'
    parameter_name = 'usuario'

    def lookups(self, request, model_admin):
        """ return options """
        
        # Generate options based in available users
        user_ids = model_admin.model.objects.all().values_list('general_point__user').distinct()
        users = [models.User.objects.filter(id=user_id[0]).first() for user_id in user_ids]
        options = tuple([(user.id, user.user_name) for user in users])
       
        return options
    
    def queryset(self, request, queryset):
        """ returns the filtered queryset """
        
        # Return all values
        if self.value() is None:
            return queryset
        
        # Get point who match with the user
        user_id = self.value()
        general_points = models.GeneralPoint.objects.filter(user_id=user_id)
        points_user = queryset.filter (general_point__in=general_points)
        
        return points_user
    
# Admin classes
@admin.register (models.User)
class AdminUser (admin.ModelAdmin):
    
    change_form_template = 'admin/change_form_users.html'    
    list_display = ('id', 'user_name', 'is_active', 'ranking', 'first_name', 'last_name', 'email', 'phone', 'user_auth')
    list_filter = ('country', 'time_zone', 'is_active', 'ranking', 'user_auth')
    ordering = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone', 'ranking', 'user_auth')
    search_fields = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone')
    search_help_text = "Buscar usuarios por nombre, apellido, email, país o zona horaria"
    ordering = ['user_name']
    list_per_page = 20

@admin.register (models.Country)
class AdminCountry (admin.ModelAdmin):
    
    list_display = ('id', 'country')
    ordering = ('id', 'country')
    search_fields = ('country', )
    list_per_page = 20
    
@admin.register (models.TimeZone)
class AdminTimeZone (admin.ModelAdmin):
    
    list_display = ('id', 'time_zone')
    ordering = ('id', 'time_zone')
    search_fields = ('time_zone', )
    list_per_page = 20
    
@admin.register (models.Stream)
class AdminStream (admin.ModelAdmin):
    
    change_form_template = 'admin/change_form_streams.html' 
    list_display = ('id', 'user', 'datetime', 'is_vip', 'is_free')
    ordering = ('id', 'user', 'datetime')
    list_filter = ('user', 'datetime', 'is_vip', 'is_free')
    search_fields = ('user__user_name', )
    list_per_page = 20
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """ render change form template for deactive fields for platinum admins """
        
        # Get admin type
        user_auth = request.user
        admin_type = tools.get_admin_type(user_auth=user_auth)
        users = models.User.objects.filter(user_auth=user_auth)
        users_ids = [f"{user.id}" for user in users]
        
        extra_context = {"admin_type": admin_type, "users_ids": users_ids}
        return super(AdminStream, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
        
    def add_view(self, request, form_url='', extra_context=None):
        """ render change form template for deactive fields for platinum admins """
        
        # Get admin typeº
        user_auth = request.user
        admin_type = tools.get_admin_type(user_auth=user_auth)
        users = models.User.objects.filter(user_auth=user_auth)
        users_ids = [f"{user.id}" for user in users]
        
        extra_context = {"admin_type": admin_type, "users_ids": users_ids}
        return super(AdminStream, self).add_view(
            request, form_url, extra_context=extra_context,
        )

    def get_queryset(self, request):
        
        # Get admin type
        user_auth = request.user
        admin_type = tools.get_admin_type(user_auth=user_auth)

        if admin_type == "admin platino":
            # Get all users of the current admin
            users = models.User.objects.filter(user_auth=user_auth)
            
            # Render only streams of the current user
            return models.Stream.objects.filter(user__in=users)
            
        # Render all streams
        return models.Stream.objects.all()     
    
@admin.register (models.Comment)
class AdminComment (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'stream', 'comment', 'datetime', 'status')
    ordering = ('id', 'user', 'stream', 'datetime', 'datetime', 'status')
    list_filter = ('user', 'datetime', 'status')
    search_fields = ('user__user_name', 'stream__user__user_name', 'comment')
    list_per_page = 20
    
@admin.register (models.WhatchCheck)
class AdminWhatchCheck (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'stream', 'datetime', 'status')
    ordering = ('id', 'user', 'stream', 'datetime', 'status')
    list_filter = ('user', 'datetime', 'status')
    search_fields = ('user__user_name', 'stream__user__user_name')
    list_per_page = 20
    
@admin.register (models.Status)
class AdminStatus (admin.ModelAdmin):
    
    list_display = ('id', 'name')
    ordering = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20

@admin.register (models.InfoPoint)
class AdminInfoPoint (admin.ModelAdmin):
    
    list_display = ('id', 'info')
    ordering = ('id', 'info')
    search_fields = ('info',)
    list_per_page = 20
    
@admin.register (models.GeneralPoint)
class AdminGeneralPoint (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount', 'stream', 'info', 'datetime')
    ordering = ('id', 'user', 'amount', 'stream', 'info', 'datetime')
    list_filter = ('info', 'datetime', 'user')
    search_fields = ('user__user_name', 'stream__user__user_name')
    list_per_page = 20
    
@admin.register (models.WeeklyPoint)
class AdminWeeklyPoint (admin.ModelAdmin):
    
    raw_id_fields = ('general_point',)
    list_display = ('id', 'general_point')
    ordering = ('id', 'general_point')
    list_filter = (FilterWeeklyDailyPoints,)
    search_fields = ('general_point__user__user_name', 'general_point__stream__user__user_name')
    list_per_page = 20
    
@admin.register (models.DailyPoint)
class AdminDailyPoint (admin.ModelAdmin):
    
    raw_id_fields = ('general_point',)
    list_display = ('id', 'general_point')
    ordering = ('id', 'general_point')
    list_filter = (FilterWeeklyDailyPoints,)
    search_fields = ('general_point__user__user_name', 'general_point__stream__user__user_name')
    list_per_page = 20
    
@admin.register (models.Ranking)
class AdminRanking (admin.ModelAdmin):
    
    list_display = ('id', 'name', 'points', 'max_streams', 'open_hour')
    ordering = ('id', 'name', 'points', 'max_streams', 'open_hour')
    search_fields = ('name',)
    list_per_page = 20
    
@admin.register (models.PointsHistory)
class AdminPointsHistory (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'general_points_num', 'general_points_week_num', 'week_points_num')
    ordering = ('id', 'user', 'general_points_num', 'general_points_week_num', 'week_points_num')
    search_fields = ('user__user_name',)
    list_per_page = 20
    
@admin.register (models.Bit)
class AdminBit (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'timestamp', 'amount', 'is_bits_done', 'details', )
    ordering = ('id', 'user', 'timestamp', 'is_bits_done', 'amount')
    list_filter = ('user', 'timestamp', 'is_bits_done', 'details',)
    search_fields = ('user__user_name', 'details')
    list_per_page = 20
    
@admin.register (models.TopDailyPoint)
class AdminTopDailyPoint (admin.ModelAdmin):
    
    list_display = ('position', 'user', 'datetime')
    ordering = ('position', 'user', 'datetime')
    list_filter = ('user', 'datetime')
    search_fields = ('user__user_name',)
    list_per_page = 20
    
@admin.register (models.StreamExtra)
class AdminStreamExtra (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount',)
    ordering = ('id', 'user', 'amount')
    list_filter = ('user',)
    search_fields = ('user__user_name',)
    list_per_page = 20
    
@admin.register (models.StreamVip)
class AdminVips (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount')
    ordering = ('id', 'user', 'amount')
    list_filter = ('user',)
    search_fields = ('user',)
    list_per_page = 20
    
@admin.register (models.Settings)
class AdminSettings (admin.ModelAdmin):
    
    list_display = ('id', 'name', 'value')
    ordering = ('id', 'name', 'value')
    search_fields = ('name', 'value')
    list_per_page = 20