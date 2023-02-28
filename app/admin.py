from . import models 
from django.contrib import admin

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
    list_display = ('id', 'user_name', 'is_active', 'ranking', 'first_name', 'last_name', 'email', 'phone', 'admin_type')
    list_filter = ('country', 'time_zone', 'is_active', 'ranking', 'admin_type')
    ordering = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone', 'ranking', 'admin_type')
    search_fields = ('id', 'user_name', 'first_name', 'last_name', 'email', 'phone')
    search_help_text = "Buscar usuarios por nombre, apellido, email, país o zona horaria"
    ordering = ['user_name']

@admin.register (models.Country)
class AdminCountry (admin.ModelAdmin):
    
    list_display = ('id', 'country')
    ordering = ('id', 'country')
    search_fields = ('country', )
    
@admin.register (models.TimeZone)
class AdminTimeZone (admin.ModelAdmin):
    
    list_display = ('id', 'time_zone')
    ordering = ('id', 'time_zone')
    search_fields = ('time_zone', )
    
@admin.register (models.Stream)
class AdminStream (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'datetime', 'is_vip', 'is_free')
    ordering = ('id', 'user', 'datetime')
    list_filter = ('user', 'datetime', 'is_vip', 'is_free')
    search_fields = ('user__user_name', )
    
@admin.register (models.Comment)
class AdminComment (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'stream', 'comment', 'datetime', 'status')
    ordering = ('id', 'user', 'stream', 'datetime', 'datetime', 'status')
    list_filter = ('user', 'datetime', 'status')
    search_fields = ('user__user_name', 'stream__user__user_name', 'comment')
    
@admin.register (models.WhatchCheck)
class AdminWhatchCheck (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'stream', 'datetime', 'status')
    ordering = ('id', 'user', 'stream', 'datetime', 'status')
    list_filter = ('user', 'datetime', 'status')
    search_fields = ('user__user_name', 'stream__user__user_name')
    
@admin.register (models.Status)
class AdminStatus (admin.ModelAdmin):
    
    list_display = ('id', 'name')
    ordering = ('id', 'name')
    search_fields = ('name',)

@admin.register (models.InfoPoint)
class AdminInfoPoint (admin.ModelAdmin):
    
    list_display = ('id', 'info')
    ordering = ('id', 'info')
    search_fields = ('info',)
    
@admin.register (models.GeneralPoint)
class AdminGeneralPoint (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount', 'stream', 'info', 'datetime')
    ordering = ('id', 'user', 'amount', 'stream', 'info', 'datetime')
    list_filter = ('user', 'stream', 'info', 'datetime')
    search_fields = ('user__user_name', 'stream__user__user_name')
    
@admin.register (models.WeeklyPoint)
class AdminWeeklyPoint (admin.ModelAdmin):
    
    list_display = ('id', 'general_point')
    ordering = ('id', 'general_point')
    list_filter = (FilterWeeklyDailyPoints,)
    search_fields = ('general_point__user__user_name', 'general_point__stream__user__user_name')
    
@admin.register (models.DailyPoint)
class AdminDailyPoint (admin.ModelAdmin):
    
    list_display = ('id', 'general_point')
    ordering = ('id', 'general_point')
    list_filter = (FilterWeeklyDailyPoints,)
    search_fields = ('general_point__user__user_name', 'general_point__stream__user__user_name')
    
@admin.register (models.Ranking)
class AdminRanking (admin.ModelAdmin):
    
    list_display = ('id', 'name', 'points', 'max_streams')
    ordering = ('id', 'name', 'points', 'max_streams')
    search_fields = ('name',)
    
@admin.register (models.PointsHistory)
class AdminPointsHistory (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'general_points', 'week_points')
    ordering = ('id', 'user', 'general_points', 'week_points')
    search_fields = ('user__user_name',)
    
@admin.register (models.Bits)
class AdminBits (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount')
    ordering = ('id', 'user', 'amount')
    list_filter = ('user',)
    search_fields = ('user__user_name',)
    
@admin.register (models.TopDailyPoint)
class AdminTopDailyPoint (admin.ModelAdmin):
    
    list_display = ('position', 'user', 'datetime')
    ordering = ('position', 'user', 'datetime')
    list_filter = ('user', 'datetime')
    search_fields = ('user__user_name',)
    
@admin.register (models.StreamExtra)
class AdminStreamExtra (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount',)
    ordering = ('id', 'user', 'amount')
    list_filter = ('user',)
    search_fields = ('user__user_name',)
    
@admin.register (models.AdminType)
class AdminAdminType (admin.ModelAdmin):
    
    list_display = ('id', 'name', 'ranking')
    ordering = ('id', 'name', 'ranking')
    list_filter = ('name', 'ranking')
    search_fields = ('name', 'ranking__name')
    
@admin.register (models.StreamVip)
class AdminVips (admin.ModelAdmin):
    
    list_display = ('id', 'user', 'amount')
    ordering = ('id', 'user', 'amount')
    list_filter = ('user',)
    search_fields = ('user',)